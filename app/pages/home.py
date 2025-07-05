import streamlit as st
import pandas as pd
from utils.ui_calendar import render_calendar_with_records
from utils.components import show_pfc_selected_date
from utils.helpers import ask_user_id, init_session_state

if "user_id" in st.session_state:
    st.query_params["user"] = st.session_state.user_id

    # session_stateの初期化
    init_session_state()

    with st.container():
        st.title("PFC MANAGEMENT")

        today_records = show_pfc_selected_date()

        render_calendar_with_records()

        if today_records:
            df = pd.DataFrame(today_records)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records yet.")
else:
    ask_user_id()
