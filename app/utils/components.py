import streamlit as st
from datetime import date
from utils.helpers import get_records_by_date, get_total_by_date

def show_pfc_selected_date():

    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)
    with col2:
        st.write("")
        selected_date = st.date_input("Date", value=date.today(), key="date_input")
        selected_date_str = selected_date.isoformat()
        select_day_records = get_records_by_date(selected_date_str)
        kcal, p, f, c = get_total_by_date(select_day_records)

    with col1:
        st.metric("カロリー", f"{kcal:.0f} kcal", border=True)
    with col3:
        st.metric("P（たんぱく質）", f"{p:.1f} g", border=True)
    with col4:
        st.metric("F（脂質）", f"{f:.1f} g", border=True)
    with col5:
        st.metric("C（炭水化物）", f"{c:.1f} g", border=True)

    return select_day_records


# def create_input(label, key, input_type="text", options=None, max_value=None, session_name="form_data"):
#     slider_key = f"{key}_slider"
#     input_key = f"{key}_input"

#     def slider_changed():
#         st.session_state[session_name][key] = round(st.session_state[slider_key],1) if input_type == "slider" else st.session_state[slider_key]

#     def input_changed():
#         st.session_state[session_name][key] = round(st.session_state[input_key], 1) if input_type == "slider" else st.session_state[input_key]

#     if input_type == "text":
#         st.text_input(label, key=input_key, on_change=input_changed)

#     elif input_type == "radio":
#         st.radio(label, options, horizontal=True, key=input_key, on_change=input_changed)
    
#     elif input_type == "slider":

#         current_value = st.session_state[session_name].get(key, 0.0)
#         if current_value > max_value:
#             current_value = 0.0
#             st.session_state[session_name][key] = current_value

#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.slider(
#                 label=label,
#                 min_value=0.0,
#                 max_value=max_value,
#                 step=0.1,
#                 value=current_value,
#                 key=slider_key,
#                 on_change=slider_changed,
#                 format="%.1f"
#             )
#         with col2:
#             st.number_input(
#                 "手入力",
#                 min_value=0.0,
#                 max_value=max_value,
#                 step=0.1,
#                 value=current_value,
#                 key=input_key,
#                 on_change=input_changed,
#                 label_visibility="hidden"
#             )

def create_input(label, key, input_type="text", options=None, max_value=None, session_name="form_data", value_type=float):
    slider_key = f"{key}_slider"
    input_key = f"{key}_input"

    def slider_changed():
        value = st.session_state[slider_key]
        if input_type != "slider":
            st.session_state[session_name][key] = value
        else:
            st.session_state[session_name][key] = round(float(value), 1) if value_type == float else int(value)

    def input_changed():
        value = st.session_state[input_key]
        if input_type != "slider":
            st.session_state[session_name][key] = value
        else:
            st.session_state[session_name][key] = round(float(value), 1) if value_type == float else int(value)

    if input_type == "text":
        st.text_input(label, key=input_key, on_change=input_changed)

    elif input_type == "radio":
        st.radio(label, options, horizontal=True, key=input_key, on_change=input_changed)
    
    elif input_type == "slider":
        current_value = st.session_state[session_name].get(key, 0.0)
        if current_value > max_value:
            current_value = 0.0
            st.session_state[session_name][key] = current_value

        col1, col2 = st.columns([2, 1])
        with col1:
            st.slider(
                label=label,
                min_value=0 if value_type == int else 0.0,
                max_value=max_value,
                step=1 if value_type == int else 0.1,
                value=int(current_value) if value_type == int else float(current_value),
                key=slider_key,
                on_change=slider_changed,
                format="%d" if value_type == int else "%.1f"
            )
        with col2:
            st.number_input(
                "手入力",
                min_value=0 if value_type == int else 0.0,
                max_value=max_value,
                step=1 if value_type == int else 0.1,
                value=int(current_value) if value_type == int else float(current_value),
                key=input_key,
                on_change=input_changed,
                label_visibility="hidden"
            )