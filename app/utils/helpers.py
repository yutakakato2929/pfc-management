from datetime import date
import pandas as pd
import streamlit as st
import os
from utils.db import select_all_records, select_all_ingredients

BASE_DIR = os.path.dirname(__file__)

# 今日日付取得
def get_today_str():
    return date.today().isoformat()

# 食べたものを日にちで取得（リスト）
def get_records_by_date(str_date):
    records = st.session_state.consumption_records
    filtered_records = [
        v for v in records.values() if v["date"] == str_date
    ]
    return filtered_records

# 対象リストの合計を取得
def get_total_by_date(records):
    df = pd.DataFrame(records)
    if df.empty:
        return 0, 0, 0, 0
    return (
        df["kcal"].sum(),
        df["protein"].sum(),
        df["fat"].sum(),
        df["carb"].sum()
    )

# SQLiteからデータを取得して、セッション状態を初期化
def init_session_state():

    consumption_records = select_all_records()
    ingredients = select_all_ingredients()
    if "ingredients" not in st.session_state:
        st.session_state.ingredients = {
            item["id"]: {k: v for k, v in item.items() if k != "id"}
            for item in ingredients
        }
    if "consumption_records" not in st.session_state:
        st.session_state.consumption_records = {
            item["id"]: {k: v for k, v in item.items() if k != "id"}
            for item in consumption_records
        }