from typing import Dict, Union, List
from collections import Counter
import pandas as pd
import numpy as np
import streamlit as st
import io
import os
import tarfile
import gzip
from cryptography.fernet import Fernet


from draw_poomsae import process_athletes
from athlete import Athlete
from match import Match
from poomsae import Poomsae


ATHLETES_FILE_COL = "athletes_file"
DRAW_FILE_COL = "draw_file"

ATHLETE_INT_COLS = ["athlete_id"]
DRAW_INT_COLS = [
    "match_id",
    "first_athlete_id",
    "second_athlete_id",
    "winner",
    "first_poomsae",
    "second_poomsae",
]


@st.cache_resource
def prepare_data_dir() -> str:
    """Decrypts the encrypted tar.gz once per process and extracts to /tmp/data."""
    ARCHIVE_PATH = "secure/data.tar.gz.enc"  # tracked in git (encrypted)
    EXTRACT_DIR = "/tmp/data"  # ephemeral runtime location

    # 1) Read encrypted blob from repo
    with open(ARCHIVE_PATH, "rb") as f:
        enc = f.read()

    # 2) Decrypt
    key_b64 = (
        st.secrets["FERNET_KEY"].encode()
        if isinstance(st.secrets["FERNET_KEY"], str)
        else st.secrets["FERNET_KEY"]
    )
    f = Fernet(key_b64)
    tar_gz_bytes = f.decrypt(enc)

    # 3) Extract to /tmp/data
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    with gzip.GzipFile(fileobj=io.BytesIO(tar_gz_bytes), mode="rb") as gz:
        with tarfile.open(fileobj=gz, mode="r:*") as tar:
            tar.extractall(
                path="/tmp"
            )  # archive root is "data/", so it lands at /tmp/data

    return EXTRACT_DIR


def read_csv(csv_path: str, int_cols: List[str] = []) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype("Int64")
    return df


def resolve_athlete_from_source(
    source_value, draw_df: pd.DataFrame, athletes: Dict[int, Athlete]
) -> tuple:
    """
    Resolves athlete ID from a source like 'W1' (winner of match 1).

    Args:
        source_value: The source value (e.g., 'W1', 'W2')
        draw_df: DataFrame containing the match draw information
        athletes: Dictionary mapping athlete IDs to Athlete objects

    Returns:
        tuple: (athlete_id, display_name) where athlete_id can be None if not yet determined
    """
    if (
        pd.notna(source_value)
        and isinstance(source_value, str)
        and source_value.startswith("W")
    ):
        try:
            source_match_id = int(source_value[1:])
            # Find the source match in the draw
            source_match = draw_df[draw_df["match_id"] == source_match_id]
            if not source_match.empty:
                winner_id = source_match.iloc[0]["winner"]
                if pd.notna(winner_id):
                    winner_id = int(winner_id)
                    if winner_id in athletes:
                        winner_athlete = athletes[winner_id]
                        return (
                            winner_id,
                            f"{winner_athlete.first_name} {winner_athlete.last_name}",
                        )
                # Winner not yet determined
                return None, f"Winner of Match {source_match_id}"
        except (ValueError, KeyError):
            pass
    return None, "TBD"


def get_categories_mapping(
    categories_csv_path: str,
) -> Dict[str, Dict[str, pd.DataFrame]]:
    df = pd.read_csv(categories_csv_path)

    mapping = {}
    all_athletes = []

    # Get the base directory from categories_csv_path (e.g., /tmp/data)
    import os

    base_dir = os.path.dirname(categories_csv_path)

    for _, row in df.iterrows():
        categ_name, athletes_file, draw_file = row

        # Convert relative paths to absolute paths based on base_dir
        # If path starts with "data/", replace it with base_dir
        if athletes_file.startswith("data/"):
            athletes_file = os.path.join(
                base_dir, athletes_file.replace("data/", "", 1)
            )
        if draw_file.startswith("data/"):
            draw_file = os.path.join(base_dir, draw_file.replace("data/", "", 1))

        draw_info = read_csv(draw_file, int_cols=DRAW_INT_COLS)
        athletes_info = read_csv(athletes_file, int_cols=ATHLETE_INT_COLS)
        athletes = process_athletes(athletes_info)

        mapping[categ_name] = {
            "athletes": athletes,
            "draw": draw_info,
            "draw_path": draw_file,
        }

        all_athletes.extend(athletes.values())

    init_poomsae_tracking(all_athletes)

    return mapping


def save_winner(draw_csv_path: str, match_id: int, winner_athlete_id: int) -> None:
    df = read_csv(draw_csv_path, int_cols=DRAW_INT_COLS)

    mask = df["match_id"] == match_id
    match_count = mask.sum()

    if match_count == 0:
        raise ValueError(f"Match id {match_id} not found in {draw_csv_path}")
    if match_count > 1:
        raise ValueError(
            f"Multiple entries found for match id {match_id} in {draw_csv_path}"
        )

    df.loc[mask, "winner"] = winner_athlete_id

    # Update future matches that reference this match as a source
    source_ref = f"W{match_id}"
    if "first_source" in df.columns:
        first_source_mask = df["first_source"] == source_ref
        df.loc[first_source_mask, "first_athlete_id"] = winner_athlete_id

    if "second_source" in df.columns:
        second_source_mask = df["second_source"] == source_ref
        df.loc[second_source_mask, "second_athlete_id"] = winner_athlete_id

    df.to_csv(draw_csv_path, index=False)


def save_poomsae(
    draw_csv_path: str, match_id: int, first_poomsae: int, second_poomsae: int
) -> None:
    df = read_csv(draw_csv_path, int_cols=DRAW_INT_COLS)
    # match_id is already Int64 from read_csv
    mask = df["match_id"] == match_id
    df.loc[mask, "first_poomsae"] = first_poomsae
    df.loc[mask, "second_poomsae"] = second_poomsae
    df.to_csv(draw_csv_path, index=False)


def find_next_match(
    draw_df: pd.DataFrame, athletes: Dict[int, Athlete], draw_path: str
) -> Union[Match, None]:
    future_matches = draw_df[draw_df["winner"].isna()]
    if future_matches.empty:
        return None

    next_match = future_matches.iloc[0]
    athlete1_id = next_match["first_athlete_id"]
    athlete2_id = next_match["second_athlete_id"]

    # Check if athlete IDs are missing and resolve from sources if needed
    if pd.isna(athlete1_id) or pd.isna(athlete2_id):
        first_source = next_match.get("first_source")
        second_source = next_match.get("second_source")

        # Check if sources can be resolved
        if pd.isna(athlete1_id) and (pd.isna(first_source) or first_source == "NA"):
            raise ValueError(
                f"First athlete ID not found for match {int(next_match['match_id'])}. Check if previous matches are finished."
            )
        if pd.isna(athlete2_id) and (pd.isna(second_source) or second_source == "NA"):
            raise ValueError(
                f"Second athlete ID not found for match {int(next_match['match_id'])}. Check if previous matches are finished."
            )

        # If we have sources, the athlete IDs should have been updated by save_winner
        # This means the source match is not yet completed
        raise ValueError(
            f"Match {int(next_match['match_id'])} cannot start yet. Waiting for previous matches to complete."
        )

    athlete1 = athletes[int(athlete1_id)]
    athlete2 = athletes[int(athlete2_id)]
    match_id = int(next_match["match_id"])

    # Convert poomsae numbers to Poomsae objects if present
    from poomsae import Poomsae

    first_poomsae = None
    if "first_poomsae" in next_match and pd.notna(next_match["first_poomsae"]):
        first_poomsae = Poomsae(number=int(next_match["first_poomsae"]))
    second_poomsae = None
    if "second_poomsae" in next_match and pd.notna(next_match["second_poomsae"]):
        second_poomsae = Poomsae(number=int(next_match["second_poomsae"]))

    match = Match(match_id, athlete1, athlete2, first_poomsae, second_poomsae)
    if match.first_poomsae and match.second_poomsae:
        return match

    match.draw_poomsae_for_match()

    # Ensure poomsae columns exist in DataFrame
    if "first_poomsae" not in draw_df.columns:
        draw_df["first_poomsae"] = np.nan
    if "second_poomsae" not in draw_df.columns:
        draw_df["second_poomsae"] = np.nan

    save_poomsae(
        draw_csv_path=draw_path,
        match_id=match.match_id,
        first_poomsae=match.first_poomsae.number(),
        second_poomsae=match.second_poomsae.number(),
    )

    return match


def init_poomsae_tracking(athletes: List[Athlete]) -> None:
    if (
        "poomsae_availability" in st.session_state
        and "poomsae_usage_counts" in st.session_state
    ):
        return  # already initialized

    max_poomsae = max(athlete.max_poomsae.number() for athlete in athletes)

    # Counts of how many athletes can perform each poomsae
    availability_counter = Counter()

    for athlete in athletes:
        min_num = athlete.min_poomsae.number()
        max_num = athlete.max_poomsae.number()

        for poomsae_num in range(min_num, max_num + 1):
            availability_counter[poomsae_num] += 1

    # Index 0 represents Poomsae 1, index 1 represents Poomsae 2, etc.
    poomsae_availability = []
    for poomsae_num in range(1, max_poomsae + 1):
        if poomsae_num in availability_counter:
            poomsae_availability.append(availability_counter[poomsae_num])
        else:
            # If no athlete can perform this poomsae, set to 1 (shouldn't happen)
            poomsae_availability.append(1)

    poomsae_availability_total = sum(poomsae_availability)
    poomsae_availability_prop = [
        count / poomsae_availability_total for count in poomsae_availability
    ]

    poomsae_usage_counts = [1] * max_poomsae

    # Store both in session state
    st.session_state["poomsae_availability"] = poomsae_availability_prop
    st.session_state["poomsae_usage_counts"] = poomsae_usage_counts
