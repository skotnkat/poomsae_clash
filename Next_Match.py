import streamlit as st
import utility
import css_utility

st.set_page_config(page_title="Poomsae Clash", layout="wide")
css_utility.set_css("main")

CATEGORIES_CSV = "data/categories.csv"

# ---- UI ----
st.title("🥋 Poomsae Clash: Next Match")
categories_map = utility.get_categories_mapping(CATEGORIES_CSV)
category_names = list(categories_map.keys())

with st.sidebar:
    st.header("Filters")
    selected_category = st.selectbox("Select a category", options=category_names)

cur_draw = categories_map[selected_category]["draw"]
cur_athletes = categories_map[selected_category]["athletes"]
cur_draw_path = categories_map[selected_category]["draw_path"]

match = utility.find_next_match(cur_draw, cur_athletes, cur_draw_path)
if match is None:
    st.warning("All matches finished!")
    st.stop()

## CSS is now set via css_utility.set_css("main")

st.markdown(
    f"<div class='category-label'>Category: {selected_category}</div>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div class='section-label'>Match {match.match_id}</div>", unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown(
        f"""
        <div class="athlete-box blue">
            <div class="athlete-name">{match.first_athlete.first_name} {match.first_athlete.last_name}</div>
            <div class="athlete-meta">Blue • ID {match.first_athlete.athlete_id}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="athlete-box red">
            <div class="athlete-name">{match.second_athlete.first_name} {match.second_athlete.last_name}</div>
            <div class="athlete-meta">Red • ID {match.second_athlete.athlete_id}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>Drawn Poomsae</div>", unsafe_allow_html=True)
pc1, pc2 = st.columns(2, gap="small")
with pc1:
    st.markdown(
        f"<div class='poomsae-box'>{match.first_poomsae.name()}</div>",
        unsafe_allow_html=True,
    )
with pc2:
    st.markdown(
        f"<div class='poomsae-box'>{match.second_poomsae.name()}</div>",
        unsafe_allow_html=True,
    )

# Winner selection and submission (simplified)
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>Winner</div>", unsafe_allow_html=True)

winner_options = {
    "None": None,
    f"🔵 Blue: {match.first_athlete.first_name} {match.first_athlete.last_name}": match.first_athlete.athlete_id,
    f"🔴 Red: {match.second_athlete.first_name} {match.second_athlete.last_name}": match.second_athlete.athlete_id,
}

# Create columns with 30% for winner selection, 70% empty
winner_col, _ = st.columns([0.3, 0.7])

with winner_col:
    selected_label = st.selectbox(
        "Select the winner",
        options=list(winner_options.keys()),
        index=0,
    )
    selected_winner_id = winner_options[selected_label]

    submitted = st.button(
        "Submit winner",
        disabled=(selected_winner_id is None),
        key=f"submit_winner_{match.match_id}",
    )
    if submitted:
        utility.save_winner(cur_draw_path, match.match_id, selected_winner_id)
        st.success("Winner saved")
        st.rerun()
