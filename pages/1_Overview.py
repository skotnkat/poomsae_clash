import streamlit as st
import pandas as pd
import utility
from utility import resolve_athlete_from_source
import css_utility


st.set_page_config(page_title="Poomsae Clash", layout="wide")
css_utility.set_css("overview")

CATEGORIES_CSV = "data/categories.csv"

# ---- UI ----
st.title("🥋 Poomsae Clash: Overview")

categories_map = utility.get_categories_mapping(CATEGORIES_CSV)
category_names = list(categories_map.keys())

with st.sidebar:
    st.header("Filters")
    selected_category = st.selectbox("Select a category", options=category_names)

cur_draw = categories_map[selected_category]["draw"]
cur_athletes = categories_map[selected_category]["athletes"]

## CSS is now set via css_utility.set_css("overview")

st.markdown(
    f"<div class='category-label'>Category: {selected_category}</div>",
    unsafe_allow_html=True,
)

# Display all matches
if cur_draw.empty:
    st.warning("No matches found for this category.")
else:
    # Function to render a single match card
    def render_match_card(match_row):
        match_id = int(match_row["match_id"])
        first_athlete_id = match_row["first_athlete_id"]
        second_athlete_id = match_row["second_athlete_id"]
        first_source = match_row.get("first_source")
        second_source = match_row.get("second_source")

        # Get first athlete info
        first_is_pending = False
        if pd.notna(first_athlete_id):
            first_athlete = cur_athletes[int(first_athlete_id)]
            first_athlete_name = f"{first_athlete.first_name} {first_athlete.last_name}"
        elif pd.notna(first_source) and first_source != "NA":
            _, first_athlete_name = resolve_athlete_from_source(
                first_source, cur_draw, cur_athletes
            )
            first_is_pending = "Winner of Match" in first_athlete_name
        else:
            first_athlete_name = "TBD"

        # Get second athlete info
        second_is_pending = False
        if pd.notna(second_athlete_id):
            second_athlete = cur_athletes[int(second_athlete_id)]
            second_athlete_name = (
                f"{second_athlete.first_name} {second_athlete.last_name}"
            )
        elif pd.notna(second_source) and second_source != "NA":
            _, second_athlete_name = resolve_athlete_from_source(
                second_source, cur_draw, cur_athletes
            )
            second_is_pending = "Winner of Match" in second_athlete_name
        else:
            second_athlete_name = "TBD"

        # Get poomsae info
        first_poomsae = "TBD"
        second_poomsae = "TBD"
        if "first_poomsae" in match_row and pd.notna(match_row["first_poomsae"]):
            from poomsae import Poomsae

            first_poomsae = Poomsae(number=int(match_row["first_poomsae"])).name()
        if "second_poomsae" in match_row and pd.notna(match_row["second_poomsae"]):
            from poomsae import Poomsae

            second_poomsae = Poomsae(number=int(match_row["second_poomsae"])).name()

        # Get winner info
        winner_text = "TBD"
        winner_class = ""
        if "winner" in match_row and pd.notna(match_row["winner"]):
            winner_id = int(match_row["winner"])
            if winner_id in cur_athletes:
                winner_athlete = cur_athletes[winner_id]
                winner_text = f"{winner_athlete.first_name} {winner_athlete.last_name}"
                # Determine winner color based on athlete position
                if pd.notna(first_athlete_id) and winner_id == int(first_athlete_id):
                    winner_class = "winner-blue"
                elif pd.notna(second_athlete_id) and winner_id == int(
                    second_athlete_id
                ):
                    winner_class = "winner-red"

        # Return match card HTML
        first_class = "tbd" if first_athlete_name == "TBD" else ""
        second_class = "tbd" if second_athlete_name == "TBD" else ""

        return f"""
            <div class="match-card">
                <div class="section-label">Match {match_id}</div>
                <div class="athletes-container">
                    <div class="athlete-row blue-athlete">
                        <span class="{first_class}">{first_athlete_name}</span>
                    </div>
                    <div class="athlete-row red-athlete">
                        <span class="{second_class}">{second_athlete_name}</span>
                    </div>
                </div>
                <div class="poomsae-info">
                    <div class="poomsae-item">
                        <div class="poomsae-label">First Poomsae</div>
                        <div class="poomsae-value {'tbd' if first_poomsae == 'TBD' else ''}">{first_poomsae}</div>
                    </div>
                    <div class="poomsae-item">
                        <div class="poomsae-label">Second Poomsae</div>
                        <div class="poomsae-value {'tbd' if second_poomsae == 'TBD' else ''}">{second_poomsae}</div>
                    </div>
                </div>
                <div class="winner-info {winner_class}">
                    <strong>Winner:</strong> <span class="{'tbd' if winner_text == 'TBD' else ''}">{winner_text}</span>
                </div>
            </div>
            """

    # Display matches in 2-column layout
    matches_list = list(cur_draw.iterrows())
    for i in range(0, len(matches_list), 2):
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            _, match_row1 = matches_list[i]
            st.markdown(render_match_card(match_row1), unsafe_allow_html=True)

        with col2:
            if i + 1 < len(matches_list):
                _, match_row2 = matches_list[i + 1]
                st.markdown(render_match_card(match_row2), unsafe_allow_html=True)

st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
