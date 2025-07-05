import streamlit as st
import pandas as pd
from utils.db import insert_consumption
from utils.components import show_pfc_selected_date, create_input

# フォームデータの初期化
def init_add_calorie():
    default_data = {
        "amount": 0.0
    }
    st.session_state["add_calorie"] = default_data

# 初期化
if "add_calorie" not in st.session_state:
    init_add_calorie()

# タイトル
st.title("カロリー記録")

# 対象日付の総カロリー表示
today_records = show_pfc_selected_date()

# 食べたものを具体表示
if today_records:
    df = pd.DataFrame(today_records)
    st.dataframe(df, use_container_width=True)

# 食材選択
st.subheader("食べたものを追加")
df = pd.DataFrame(st.session_state.ingredients).T
selected = st.selectbox("食材を選択", df["name"].tolist())
if selected:
    st.dataframe(df[df["name"] == selected], use_container_width=True)
# 選択された食材情報取得
selected_row = df[df["name"] == selected].iloc[0]

# 単位に応じた最大値を動的に設定
unit = selected_row["unit"]
max_amount = 1000.0 if unit == "g" else 10
type = float if unit == "g" else int

create_input(f"何{unit} 食べましたか？", "amount", input_type="slider", max_value=max_amount, session_name="add_calorie", value_type=type)

if st.button("追加"):
    factor = st.session_state["add_calorie"]["amount"] / selected_row["amount"]
    record = {
        "date": st.session_state.date_input.isoformat(),
        "ingredient_id": int(selected_row.name),
        "quantity": st.session_state["add_calorie"]["amount"],
        "kcal": round(selected_row["kcal"] * factor, 1),
        "protein": round(selected_row["protein"] * factor, 1),
        "fat": round(selected_row["fat"] * factor, 1),
        "carb": round(selected_row["carb"] * factor, 1),
    }
    record_id = insert_consumption(record)

    record["name"] = selected_row["name"]
    record["unit"] = selected_row["unit"]
    st.session_state["consumption_records"][record_id] = record
    init_add_calorie()
    st.rerun()