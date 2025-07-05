from datetime import date
import pandas as pd
import streamlit as st
import os
import uuid
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

    consumption_records = select_all_records(st.session_state.user_id)
    ingredients = select_all_ingredients(st.session_state.user_id)
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

def ask_user_id():
    st.title("PFCアプリへようこそ")
    user_input = st.text_input("ユーザーIDを入力してください（例: mydiet2025）", key="user_input")
    
    if st.button("開始"):
        if user_input:
            st.session_state.user_id = user_input
            st.query_params["user"] = user_input
            st.rerun()
        else:
            st.error("ユーザーIDを入力してください")

def get_user_id():
    if "user_id" in st.session_state:
        st.query_params["user"] = st.session_state.user_id
        return st.session_state.user_id
    else:
        st.switch_page("pages/home.py")