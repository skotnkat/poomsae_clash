import streamlit as st

import utility
from draw_poomsae import POOMSAE_NUMBER_TO_NAME_MAP, Athlete, get_poomsae_for_match


st.set_page_config(page_title="Categories Starter", layout="wide")

CATEGORIES_CSV = "data/categories.csv"

# ---- UI ----
st.title("🏷️ Category Loader (Starter)")
categories_map = utility.get_categories_mapping(CATEGORIES_CSV)
category_names = list(categories_map.keys())

print(f"Loaded data:")
for category in category_names:
    print(f"- Category: {category}")
    print(f"\t Athletes: {categories_map[category]['athletes'].head()}")
    print(f"\t Draw: {categories_map[category]['draw'].head()}")

with st.sidebar:
    st.header("Filters")
    selected_category = st.selectbox("Select a category", options=category_names)


cur_draw = categories_map[selected_category]["draw"]
cur_athletes = categories_map[selected_category]["athletes"]

res = utility.find_next_match(cur_draw, cur_athletes)
if res is None:
    st.warning("All matches finished!")
    st.stop()

match_id, athlete1, athlete2 = res


print(f"Next match: {match_id}, athletes: {athlete1.athlete_id}, {athlete2.athlete_id}")

drawn_poomsae = get_poomsae_for_match(athlete1, athlete2)
print(
    f"Athlete 1: {athlete1.last_name}, min poomsae: {athlete1.min_poomsae}, max poomsae: {athlete1.max_poomsae}"
)
print(
    f"Athlete 2: {athlete2.last_name}, min poomsae: {athlete2.min_poomsae}, max poomsae: {athlete2.max_poomsae}"
)
print(f"Drawn poomsae: {drawn_poomsae}")
print("-" * 50)
