import streamlit as st
from utils.helpers import add_ingredient_to_csv

def init_session_state():
    st.session_state["form_data"] = {
        "name": "",
        "unit": "g",
        "amount": 0.0,
        "kcal": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "carb": 0.0
    }

# session_storeの初期化
if "form_data" not in st.session_state:
    init_session_state()

def make_input(label, key_prefix, type):
    input_key = f"{key_prefix}_input"

    def input_changed():
        st.session_state["form_data"][key_prefix] = st.session_state[input_key]

    if type == "radio":
        st.radio(label,["g", "個"],captions=["グラム","個数"],horizontal=True, key=input_key,
            on_change=input_changed)
    elif type == "text_input":
        st.text_input(label, key=input_key,
            on_change=input_changed)

# 各 nutrient に対応するスライダーと入力の連動関数
def make_slider_input(label, key_prefix, max_value=100.0):
    slider_key = f"{key_prefix}_slider"
    input_key = f"{key_prefix}_input"

    def slider_changed():
        st.session_state["form_data"][key_prefix] = round(st.session_state[slider_key],1)

    def input_changed():
        st.session_state["form_data"][key_prefix] = round(st.session_state[input_key],1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.slider(
            label,
            min_value=0.0,
            max_value=max_value,
            step=0.1,
            value=st.session_state["form_data"][key_prefix],
            key=slider_key,
            on_change=slider_changed,
            label_visibility="visible",
            format="%.1f"
        )
    with col2:
        st.number_input(
            "手入力",
            min_value=0.0,
            max_value=max_value,
            step=0.1,
            value=st.session_state["form_data"][key_prefix],
            key=input_key,
            on_change=input_changed,
            label_visibility="hidden",
            format="%.1f"
        )

def make_slider_dynamic_input(key_prefix, dynamic_label=None, dynamic_max=None):
    slider_key = f"{key_prefix}_slider"
    input_key = f"{key_prefix}_input"

    # ラベルと最大値を動的に取得
    label = dynamic_label or key_prefix
    max_value = dynamic_max() if callable(dynamic_max) else (dynamic_max or 100.0)

    # 現在の値を取得（なければ 0.0）
    current_value = st.session_state["form_data"].get(key_prefix, 0.0)

    # max_value を超えていたら補正
    if current_value > max_value:
        # current_value = max_value
        current_value = 0.0
        st.session_state["form_data"][key_prefix] = current_value

    def slider_changed():
        st.session_state["form_data"][key_prefix] = round(st.session_state[slider_key], 1)

    def input_changed():
        st.session_state["form_data"][key_prefix] = round(st.session_state[input_key], 1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.slider(
            label=label,
            min_value=0.0,
            max_value=max_value,
            step=0.1,
            value=current_value,
            key=slider_key,
            on_change=slider_changed,
            format="%.1f"
        )
    with col2:
        st.number_input(
            "手入力",
            min_value=0.0,
            max_value=max_value,
            step=0.1,
            value=current_value,
            key=input_key,
            on_change=input_changed,
            label_visibility="hidden"
        )

# ---------- フォーム外で数値UI ----------
st.title("食材追加")
make_input("食材名", "name", "text_input")
make_input("単位を選択", "unit", "radio")
# make_slider_input("量 (g)", "amount", 500.0)
# 例: 単位が "g" か "個" かで最大値を変える
unit = st.session_state["form_data"].get("unit", "g")

def get_max_by_unit():
    return 500.0 if unit == "g" else 10.0

make_slider_dynamic_input(
    key_prefix="amount",
    dynamic_label=f"量 ({unit})",
    dynamic_max=get_max_by_unit
)
make_slider_input("カロリー (Kcal)", "kcal", 500.0)
make_slider_input("タンパク質 (g)", "protein", 100.0)
make_slider_input("脂質 (g)", "fat", 100.0)
make_slider_input("炭水化物 (g)", "carb", 100.0)

st.write(st.session_state)
# ---------- フォームで確認して送信 ----------
with st.form("confirm_form"):
    st.subheader("送信前の確認")
    form_data = st.session_state.form_data
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("食材名", form_data["name"])
    col2.metric("量", f"{form_data["amount"]} {form_data["unit"]}")
    col3.metric("カロリー", f"{form_data["kcal"]} kcal")
    col4.metric("タンパク質", f"{form_data["protein"]} g")
    col5.metric("脂質", f"{form_data["fat"]} g")
    col6.metric("炭水化物", f"{form_data["carb"]} g")

    submitted = st.form_submit_button("記録を追加")
    if submitted:
        errors = []
        if not form_data["name"].strip():
            errors.append("食材名は必須です。")
        if form_data["amount"] == 0 or form_data["kcal"] == 0:
            errors.append("量とカロリーは 0 より大きくしてください。")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.success("登録しました！")
            add_ingredient_to_csv()
            st.rerun()