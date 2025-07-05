import streamlit as st
import pandas as pd
import os
from utils.db import insert_consumption
from utils.helpers import get_today_str, get_records_by_date, get_totals

# session_storeの初期化
if "add_calorie" not in st.session_state:
    st.session_state["add_calorie"] = 0.0

st.title("カロリー記録")

today_str = get_today_str()
today_records = get_records_by_date(today_str)
kcal, p, f, c = get_totals(today_records)

st.subheader("今日の合計")
col1, col2, col3, col4 = st.columns(4)
col1.metric("カロリー", f"{kcal:.0f} kcal")
col2.metric("P（たんぱく質）", f"{p:.1f} g")
col3.metric("F（脂質）", f"{f:.1f} g")
col4.metric("C（炭水化物）", f"{c:.1f} g")

if today_records:
    df = pd.DataFrame(today_records)
    st.dataframe(df, use_container_width=True)

st.subheader("食材を追加")
df = pd.DataFrame(st.session_state.ingredients).T
selected = st.selectbox("食材を選択", df["name"].tolist())
selected_row = df[df["name"] == selected].iloc[0]
# qty = st.number_input(f"何 {selected_row['unit']} 食べましたか？", min_value=0.0, step=0.1)
slider_key = "_slider"
input_key = "_input"

def slider_changed():
    st.session_state["add_calorie"] = round(st.session_state[slider_key],1)

def input_changed():
    st.session_state["add_calorie"] = round(st.session_state[input_key],1)

col1, col2 = st.columns([2, 1])
with col1:
    st.slider(
        f"何 {selected_row['unit']} 食べましたか？",
        min_value=0.0,
        max_value=1000.0,
        step=0.1,
        value=st.session_state["add_calorie"],
        key=slider_key,
        on_change=slider_changed,
        label_visibility="visible",
        format="%.1f"
    )
with col2:
    st.number_input(
        "手入力",
        min_value=0.0,
        max_value=1000.0,
        step=0.1,
        value=st.session_state["add_calorie"],
        key=input_key,
        on_change=input_changed,
        label_visibility="hidden",
        format="%.1f"
    )

if st.button("追加"):
    factor = st.session_state["add_calorie"] / selected_row["amount"]
    record = {
        "date": today_str,
        "ingredient_id": int(selected_row.name),
        "quantity": st.session_state["add_calorie"],
        "kcal": round(selected_row["kcal"] * factor, 1),
        "protein": round(selected_row["protein"] * factor, 1),
        "fat": round(selected_row["fat"] * factor, 1),
        "carb": round(selected_row["carb"] * factor, 1),
    }
    record_id = insert_consumption(record)

    record["name"] = selected_row["name"]
    record["unit"] = selected_row["unit"]
    st.session_state["consumption_records"][record_id] = record

    st.rerun()