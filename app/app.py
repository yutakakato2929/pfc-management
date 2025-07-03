import streamlit as st
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

def main():
    home_page = st.Page(CURRENT_DIR / "pages" / "home.py", title="ホーム", default=True)
    ui_chart_page = st.Page(CURRENT_DIR / "pages" / "ui_chart.py", title="統計")
    add_calorie_page = st.Page(CURRENT_DIR / "pages" / "add_calorie.py", title="カロリー記録")
    add_ingredients_page = st.Page(CURRENT_DIR / "pages" / "add_ingredients.py", title="食材追加")

    pg = st.navigation([home_page, ui_chart_page, add_ingredients_page, add_calorie_page], position="top")
    st.set_page_config(page_title="PFC Tracker", page_icon="🔥", layout="centered")
    pg.run()

if __name__ == "__main__":
    main()