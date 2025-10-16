from typing import Dict, Tuple, List
import pandas as pd
import datetime
import random
import streamlit as st

CUR_YEAR = datetime.datetime.now().year

JUNIOR_RANGE = range(CUR_YEAR - 17, CUR_YEAR - 14 + 1)

print(f"Junior range: {JUNIOR_RANGE}")

POOMSAE_NUMBER_TO_NAME_MAP = {
    4: "Sa Jang",
    5: "Oh Jang",
    6: "Yuk Jang",
    7: "Chil Jang",
    8: "Pal Jang",
    9: "Koryo",
    10: "Keumgang",
    11: "Taebaek",
    12: "Pyongwon",
    13: "Sipjin",
    14: "Jitae",
    15: "Cheonkwon",
    16: "Hansu",
    17: "Ilyeo",
}

POOMSAE_NAME_TO_NUMBER_MAP = {v: k for k, v in POOMSAE_NUMBER_TO_NAME_MAP.items()}


def get_min_poomsae(birth_year: int, belt_category: str) -> int:
    if belt_category == "B":
        return 4

    if birth_year in JUNIOR_RANGE:
        return 5

    return 7  # Seniors


class Athlete:
    def __init__(
        self,
        athlete_id: int,
        first_name: str,
        last_name: str,
        birth_year: int,
        category: str,
        max_poomsae: int,
    ):
        self.athlete_id = athlete_id
        self.first_name = first_name
        self.last_name = last_name

        self.min_poomsae = get_min_poomsae(birth_year, category)
        self.max_poomsae = max_poomsae


def process_athletes(athletes_df: pd.DataFrame) -> Dict[int, Athlete]:
    athletes = dict()

    for _, row in athletes_df.iterrows():
        max_poomsae_name = row["max_poomsae"]
        athlete = Athlete(
            athlete_id=row["athlete_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            birth_year=row["birth_year"],
            category=row["category"],
            max_poomsae=POOMSAE_NAME_TO_NUMBER_MAP[max_poomsae_name],
        )
        athletes[athlete.athlete_id] = athlete

    return athletes


def get_poomsae_intersection(athlete1: Athlete, athlete2: Athlete) -> Tuple[int, int]:
    min_poomsae = max(athlete1.min_poomsae, athlete2.min_poomsae)
    max_poomsae = min(athlete1.max_poomsae, athlete2.max_poomsae)
    if min_poomsae > max_poomsae:
        raise ValueError("No overlapping poomsae range")  # should never happen

    return min_poomsae, max_poomsae


def draw_poomsae(min_poomsae, max_poomsae, prev_poomsae=None):
    poomsae_counts = st.session_state["poomsae_counts"]
    poomsae_options = list(range(min_poomsae, max_poomsae + 1))
    cur_weights = [
        1 / poomsae_counts[p - 1] for p in poomsae_options
    ]  # inverse weights

    if prev_poomsae in poomsae_options:
        idx = poomsae_options.index(prev_poomsae)
        poomsae_options.remove(prev_poomsae)
        cur_weights.pop(idx)

    selected_poomsae = random.choices(
        poomsae_options,
        weights=cur_weights,
        k=1,
    )[0]

    st.session_state["poomsae_counts"][selected_poomsae - 1] += 1

    return selected_poomsae, poomsae_counts


def get_poomsae_for_match(athlete1: Athlete, athlete2: Athlete):
    min_poomsae, max_poomsae = get_poomsae_intersection(athlete1, athlete2)
    first_poomsae, poomsae_counts = draw_poomsae(
        min_poomsae,
        max_poomsae,
    )

    second_poomsae, poomsae_counts = draw_poomsae(
        min_poomsae, max_poomsae, prev_poomsae=first_poomsae
    )

    print(f"Poomsae numbers: {first_poomsae}, {second_poomsae}")
    print(
        f"Poomsae names: {POOMSAE_NUMBER_TO_NAME_MAP[first_poomsae]}, {POOMSAE_NUMBER_TO_NAME_MAP[second_poomsae]}"
    )

    return (
        first_poomsae,
        POOMSAE_NUMBER_TO_NAME_MAP[second_poomsae],
        POOMSAE_NUMBER_TO_NAME_MAP[poomsae_counts],
    )
