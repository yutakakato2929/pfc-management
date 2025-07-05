import streamlit as st
import pandas as pd
from utils.db import insert_consumption, delete_record, update_record, select_all_records
from utils.components import show_pfc_selected_date, create_input
from utils.helpers import get_user_id, COLUMNS_TO_EXCLUDE_RECORDS, COLUMNS_TO_EXCLUDE_INGREDIENTS

get_user_id()

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
disabled_list = ['name', 'unit', 'kcal', 'protein', 'fat', 'carb']
if today_records:
    df_original = pd.DataFrame(today_records)
    df_excluded = df_original.drop(columns=COLUMNS_TO_EXCLUDE_RECORDS)
    edited_df = st.data_editor(df_excluded, key="editing_records", hide_index=True, num_rows="dynamic", disabled=disabled_list)
if st.button("編集を保存"):
    deleted_rows = st.session_state.editing_records["deleted_rows"]
    added_rows = st.session_state.editing_records["added_rows"]
    edited_rows = st.session_state.editing_records["edited_rows"]
    if len(added_rows) != 0:
        st.error("削除か量の編集のみ可能です。")
    else:
        if len(deleted_rows) > 0:
            for row in deleted_rows:
                deleted_id = df_original.iloc[row]["id"]
                delete_record(int(deleted_id))
                st.session_state.consumption_records = [
                    record for record in st.session_state.consumption_records if record["id"] != deleted_id
                ]
            # st.success("削除しました。")
        
        if len(edited_rows) > 0:
            for key, value in edited_rows.items():
                update_id = df_original.iloc[key]["id"]
                update_record(int(update_id), value)
            st.session_state.consumption_records = select_all_records(st.session_state.user_id)
            # st.success("更新しました！")
        
        st.rerun()

# 食材選択
st.subheader("食べたものを追加")
df = pd.DataFrame(st.session_state.ingredients)
if df.empty:
    st.warning("まだ食材が登録されていません。先に追加してください。")
else:
    selected = st.selectbox("食材を選択", df["name"].tolist())
    if selected:
        df_excluded = df.drop(columns=COLUMNS_TO_EXCLUDE_INGREDIENTS)
        st.dataframe(df_excluded [df_excluded ["name"] == selected], use_container_width=True, hide_index=True)
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
            "ingredient_id": int(selected_row["id"]),
            "quantity": st.session_state["add_calorie"]["amount"],
            "kcal": round(selected_row["kcal"] * factor, 1),
            "protein": round(selected_row["protein"] * factor, 1),
            "fat": round(selected_row["fat"] * factor, 1),
            "carb": round(selected_row["carb"] * factor, 1),
            "user_id": st.session_state.user_id,
        }
        record_id = insert_consumption(record)

        record["name"] = selected_row["name"]
        record["unit"] = selected_row["unit"]
        record["id"] = record_id
        st.session_state["consumption_records"].append(record)
        init_add_calorie()
        st.rerun()