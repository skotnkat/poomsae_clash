from typing import Dict, Tuple, Union
import pandas as pd

import streamlit as st

from draw_poomsae import process_athletes, Athlete


ATHLETES_FILE_COL = "athletes_file"
DRAW_FILE_COL = "draw_file"


def read_csv(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path, na_values=["NA"])


def get_categories_mapping(
    categories_csv_path: str,
) -> Dict[str, Dict[str, pd.DataFrame]]:
    df = pd.read_csv(categories_csv_path)

    mapping = {}
    for _, row in df.iterrows():
        categ_name, athletes_file, draw_file = row
        athletes_info = read_csv(athletes_file)
        draw_info = read_csv(draw_file)

        athletes = process_athletes(athletes_info)
        mapping[categ_name] = {
            "athletes": athletes,
            "draw": draw_info,
        }

        st.session_state["max_poomsae"] = athletes_info["max_poomsae"].max()
        st.session_state["poomsae_counts"] = [1] * st.session_state["max_poomsae"]

    return mapping


def find_next_match(
    draw_df: pd.DataFrame, athletes: Dict[int, Athlete]
) -> Union[Tuple[int, Athlete, Athlete], None]:
    next_match = draw_df[draw_df["winner"].isna()]
    if next_match.empty:
        return None

    athlete1 = athletes[next_match["athlete1_id"]]
    athlete2 = athletes[next_match["athlete2_id"]]

    return next_match["match_id"], athlete1, athlete2
