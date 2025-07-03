from datetime import date
import pandas as pd
import streamlit as st
import logging
import os

# メインセッション系
def get_today_str():
    return date.today().isoformat()

def get_today_records():
    return st.session_state.get("records_by_date", {}).get(get_today_str(), [])

def get_totals(records):
    df = pd.DataFrame(records)
    if df.empty:
        return 0, 0, 0, 0
    return (
        df["kcal"].sum(),
        df["protein"].sum(),
        df["fat"].sum(),
        df["carb"].sum()
    )

BASE_DIR = os.path.dirname(__file__)

# @st.cache_data
def load_ingredients():
    path = os.path.join(BASE_DIR, "..", "data", "ingredients.csv")
    return pd.read_csv(path)

def add_ingredient_to_csv():
    # CSVを読み込み、次のIDを取得
    df = load_ingredients()

    # 追記する行のデータを構築
    next_id = df["id"].max() + 1
    row_data = st.session_state.form_data
    logging.error(row_data)
    
    new_row = {
        "id": next_id,
        "name": row_data["name"],
        "unit": row_data["unit"],
        "amount": row_data["amount"],
        "kcal": row_data["kcal"],
        "protein": row_data["protein"],
        "fat": row_data["fat"],
        "carbohydrate": row_data["carb"],
        "note": row_data["note"] if row_data.get("note") else ""
    }

    new_df = pd.DataFrame([new_row])
    updated_df = pd.concat([df, new_df], ignore_index=True)

    # ヘッダーの有無に応じて追記保存
    updated_df.to_csv(os.path.join(BASE_DIR, "..", "data", "ingredients.csv"), index=False)

    if "form_data" in st.session_state:
        del st.session_state["form_data"]