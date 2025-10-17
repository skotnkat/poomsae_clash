from typing import Dict, Tuple, Optional
import pandas as pd
import random
import streamlit as st

from athlete import Athlete
from poomsae import Poomsae


def process_athletes(athletes_df: pd.DataFrame) -> Dict[int, Athlete]:
    athletes = dict()

    for _, row in athletes_df.iterrows():
        max_poomsae_name = row["highest_poomsae"]

        athlete = Athlete(
            athlete_id=row["athlete_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            birth_year=row["birth_year"],
            category=row["category"],
            max_poomsae=Poomsae(name=max_poomsae_name),
        )
        athletes[athlete.athlete_id] = athlete

    return athletes


def get_poomsae_intersection(athlete1: Athlete, athlete2: Athlete) -> Tuple[int, int]:
    min_poomsae = max(athlete1.min_poomsae, athlete2.min_poomsae)
    max_poomsae = min(athlete1.max_poomsae, athlete2.max_poomsae)

    if min_poomsae > max_poomsae:
        raise ValueError("No overlapping poomsae range")  # should never happen

    return min_poomsae, max_poomsae


def draw_poomsae(
    min_poomsae: Poomsae, max_poomsae: Poomsae, prev_poomsae: Optional[Poomsae] = None
) -> Poomsae:
    usage_counts = st.session_state["poomsae_usage_counts"]
    usage_counts_total = sum(usage_counts)

    availability = st.session_state["poomsae_availability"]
    poomsae_options = list(range(min_poomsae.number(), max_poomsae.number() + 1))

    # Remove previously selected poomsae if applicable
    if prev_poomsae is not None and prev_poomsae.number() in poomsae_options:
        poomsae_options.remove(prev_poomsae.number())

    cur_weights = [
        1 / (availability[p - 1] * (2 * (usage_counts[p - 1]) / usage_counts_total))
        for p in poomsae_options
    ]

    # Normalize weights to sum to 1
    cur_weights_total = sum(cur_weights)
    cur_weights_norm = [w / cur_weights_total for w in cur_weights]

    selected_poomsae = random.choices(
        poomsae_options,
        weights=cur_weights_norm,
        k=1,
    )[0]

    st.session_state["poomsae_usage_counts"][selected_poomsae - 1] += 1

    return Poomsae(number=selected_poomsae)
