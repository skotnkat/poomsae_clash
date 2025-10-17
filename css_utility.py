# css_utility.py

# This module provides CSS style blocks for Streamlit pages.
# Usage: import css_utility and use css_utility.set_css(page="overview") or css_utility.set_css(page="main")

import streamlit as st

# Unified font and color variables
FONT_FAMILY = "'Segoe UI', 'Roboto', 'Arial', sans-serif"
PRIMARY_BLUE = "#1e90ff"
PRIMARY_RED = "#ff4136"
PRIMARY_BG = "#ffffff"
CARD_SHADOW = "0 2px 8px rgba(0,0,0,0.08)"


# CSS blocks for each page
# --- Common smaller page title ---
CSS_TITLE = """
<style>
.st-emotion-cache-10trblm, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1avcm0n, .st-emotion-cache-1dp5vir {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #444 !important;
    margin-bottom: 0.5rem !important;
}
/* Target h1 elements (st.title) more directly */
h1 {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #444 !important;
    margin-bottom: 0.5rem !important;
}
</style>
"""

CSS_OVERVIEW = f"""
<style>
  body, div, span, input, select {{
    font-family: {FONT_FAMILY};
  }}
  .category-label {{
    font-size: 1.2rem;
    font-weight: 600;
    color: #666;
    margin-bottom: 0.5rem;
  }}
  .match-card {{
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    background: {PRIMARY_BG};
    box-shadow: {CARD_SHADOW};
  }}
  .section-label {{
    font-size: 1.05rem;
    font-weight: 600;
    color: #666;
    margin: 0.25rem 0 0.75rem;
  }}
  .athletes-container {{
    display: flex;
    gap: 1rem;
    margin-bottom: 0.75rem;
  }}
  .athlete-row {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
  }}
  .blue-athlete, .red-athlete {{
    font-size: 1rem;
    font-weight: 600;
  }}
  .blue-athlete {{
    background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, #0066cc 100%);
    color: white;
    box-shadow: 0 3px 10px rgba(0,102,204,0.2);
  }}
  .red-athlete {{
    background: linear-gradient(135deg, {PRIMARY_RED} 0%, #cc2a1f 100%);
    color: white;
    box-shadow: 0 3px 10px rgba(204,42,31,0.2);
  }}
  .poomsae-info {{
    display: flex;
    gap: 1rem;
    margin: 0.75rem 0;
    padding: 0.75rem;
    background: #f8f9fa;
    border-radius: 8px;
  }}
  .poomsae-item {{
    flex: 1;
    padding: 0.3rem;
    background: white;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    text-align: center;
    font-weight: 600;
    color: #333;
  }}
  .poomsae-label {{
    font-size: 0.8rem;
    color: #666;
    margin-bottom: 0.15rem;
  }}
  .poomsae-value {{
    font-size: 0.95rem;
  }}
  .winner-info {{
    margin-top: 0.75rem;
    padding: 0.75rem;
    background: #f0f8f0;
    border-left: 4px solid #28a745;
    border-radius: 6px;
    font-weight: 600;
    color: #155724;
  }}
  .winner-blue {{
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-left: 4px solid {PRIMARY_BLUE};
    color: #0066cc;
  }}
  .winner-red {{
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    border-left: 4px solid {PRIMARY_RED};
    color: #cc2a1f;
  }}
  .tbd {{
    color: #999;
    font-style: italic;
  }}
</style>
"""

CSS_MAIN = f"""
<style>
  body, div, span, input, select {{
    font-family: {FONT_FAMILY};
  }}
  .category-label {{
    font-size: 1.2rem;
    font-weight: 600;
    color: #666;
    margin-bottom: 0.5rem;
  }}
  .section-label {{ font-size: 1.05rem; color: #666; font-weight: 600; margin: 0.25rem 0 0.75rem; }}
  .athlete-box {{ padding: 1rem; border-radius: 10px; color: #fff; text-align: center; font-family: {FONT_FAMILY}; }}
  .athlete-name {{ font-size: 1.1rem; font-weight: 600; line-height: 1.2; letter-spacing: 0.3px; }}
  .athlete-meta {{ font-size: 0.9rem; opacity: 0.95; margin-top: 0.35rem; }}
  .blue {{ background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, #0066cc 100%); box-shadow: 0 6px 18px rgba(0,102,204,0.25); }}
  .red {{ background: linear-gradient(135deg, {PRIMARY_RED} 0%, #cc2a1f 100%); box-shadow: 0 6px 18px rgba(204,42,31,0.25); }}
  .poomsae-box {{ width: 100%; padding: 1rem 1.2rem; border-radius: 10px; border: 2px solid #d0d0d0; text-align: center; color: #333; font-weight: 600; font-size: 1.05rem; background: {PRIMARY_BG}; box-shadow: 0 6px 18px rgba(0,0,0,0.06); font-family: {FONT_FAMILY}; }}
</style>
"""


def set_css(page: str):
    """
    Injects the CSS for the given page into Streamlit.
    page: "overview" or "main"
    """
    st.markdown(CSS_TITLE, unsafe_allow_html=True)
    if page == "overview":
        st.markdown(CSS_OVERVIEW, unsafe_allow_html=True)
    elif page == "main":
        st.markdown(CSS_MAIN, unsafe_allow_html=True)
    else:
        raise ValueError("Unknown page type for CSS")
