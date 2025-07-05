import streamlit as st
import pandas as pd
from utils.db import insert_ingredient, delete_ingredient, update_ingredient, select_all_ingredients
from utils.components import create_input
from utils.helpers import get_user_id, COLUMNS_TO_EXCLUDE_INGREDIENTS

get_user_id()

# フォームデータの初期化
def init_form_data():
    default_data = {
        "name": "",
        "unit": "g",
        "amount": 0.0,
        "kcal": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "carb": 0.0,
        "note": ""
    }
    st.session_state["form_data"] = default_data

# エラーチェック関数
def validate_form_data(form_data):
    errors = []
    if not form_data["name"].strip():
        errors.append("食材名は必須です。")
    if form_data["amount"] <= 0:
        errors.append("量は 0 より大きくしてください。")
    if form_data["kcal"] <= 0:
        errors.append("カロリーは 0 より大きくしてください。")
    return errors

# 初期化
if "form_data" not in st.session_state:
    init_form_data()

# タイトル
st.title("食材追加")

# 入力フィールド
create_input("食材名", "name", input_type="text")
create_input("単位を選択", "unit", input_type="radio", options=["g", "個"])

# 単位に応じた最大値を動的に設定
unit = st.session_state["form_data"].get("unit", "g")
max_amount = 500.0 if unit == "g" else 10
type = float if unit == "g" else int

create_input(f"量 ({unit})", "amount", input_type="slider", max_value=max_amount, value_type=type)
create_input("カロリー (Kcal)", "kcal", input_type="slider", max_value=500.0)
create_input("タンパク質 (g)", "protein", input_type="slider", max_value=100.0)
create_input("脂質 (g)", "fat", input_type="slider", max_value=100.0)
create_input("炭水化物 (g)", "carb", input_type="slider", max_value=100.0)
create_input("メモ", "note", input_type="text")

# ---------- フォームで確認して送信 ----------
with st.form("confirm_form"):
    st.subheader("確認")
    form_data = st.session_state.form_data

    # 確認用のメトリック表示
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("食材名", form_data["name"])
    col2.metric("量", f"{form_data["amount"]} {form_data["unit"]}")
    col3.metric("カロリー", f"{form_data["kcal"]} kcal")
    col4.metric("タンパク質", f"{form_data["protein"]} g")
    col5.metric("脂質", f"{form_data["fat"]} g")
    col6.metric("炭水化物", f"{form_data["carb"]} g")

    st.text(f"メモ: {form_data["note"]}")

    # 送信ボタン
    submitted = st.form_submit_button("記録を追加")
    if submitted:
        errors = validate_form_data(form_data)
        if errors:
            for error in errors:
                st.error(error)
        else:
            form_data["user_id"] = st.session_state.user_id
            ingredient_id = insert_ingredient(form_data)
            form_data["id"] = ingredient_id
            st.session_state["ingredients"].append(form_data)
            st.success("登録しました！")
            init_form_data()
            st.rerun()

df = pd.DataFrame(st.session_state.ingredients)
if not df.empty:
    df_excluded = df.drop(columns=COLUMNS_TO_EXCLUDE_INGREDIENTS)
    unit = ['g', '個']
    config = {
        'name' : st.column_config.TextColumn('Name', required=True),
        'unit' : st.column_config.SelectboxColumn('Unit', options=unit, required=True),
        'amount' : st.column_config.NumberColumn('Amount', required=True),
        'kcal' : st.column_config.NumberColumn('Kcal', required=True),
        'protein' : st.column_config.NumberColumn('Protein', required=True),
        'fat' : st.column_config.NumberColumn('Fat', required=True),
        'carb' : st.column_config.NumberColumn('Carb', required=True),
    }
    edited_df = st.data_editor(df_excluded, key="editing_ingredients", hide_index=True, num_rows="dynamic", column_config=config, use_container_width=True)
    if st.button("編集を保存"):
        deleted_rows = st.session_state.editing_ingredients["deleted_rows"]
        added_rows = st.session_state.editing_ingredients["added_rows"]
        edited_rows = st.session_state.editing_ingredients["edited_rows"]
        if not deleted_rows and not added_rows and not edited_rows:
            st.error("編集がありません。")
        else:
            if len(deleted_rows) > 0:
                for row in deleted_rows:
                    deleted_map = st.session_state.ingredients[row]
                    delete_ingredient(deleted_map["id"])
                result = [item for i, item in enumerate(st.session_state.ingredients) if i not in deleted_rows]
                st.session_state.ingredients = result
                st.success("削除しました。")

            if len(added_rows) > 0:
                for row in added_rows:
                    row.get("note", "")
                    row["user_id"] = st.session_state.user_id
                    ingredient_id = insert_ingredient(row)
                    row["id"] = ingredient_id
                    st.session_state["ingredients"].append(row)
                st.success("登録しました！")

            if len(edited_rows) > 0:
                for key, value in edited_rows.items():
                    update_id = st.session_state.ingredients[key]["id"]
                    update_ingredient(update_id, value)
                st.session_state.ingredients = select_all_ingredients(st.session_state.user_id)
                st.success("更新しました！")