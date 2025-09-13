import streamlit as st
import pandas as pd
from utils.ui_calendar import render_calendar_with_records
from utils.components import show_pfc_selected_date
from utils.helpers import ask_user_id, init_session_state, COLUMNS_TO_EXCLUDE_RECORDS

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
            df_excluded = df.drop(columns=COLUMNS_TO_EXCLUDE_RECORDS)
            st.dataframe(df_excluded, use_container_width=True, hide_index=True)
        else:
            st.info("No records yet.")

        # for i in range(6):
        #     cols = st.columns(7)
        #     for col in cols:
        #         with col:
        #             st.write("カロリー")
else:
    ask_user_id()
