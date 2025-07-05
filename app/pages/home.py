import streamlit as st
import pandas as pd
from utils.ui_calendar import render_calendar_with_records
from utils.components import show_pfc_selected_date

with st.container():
    st.title("PFC MANAGEMENT")

    today_records = show_pfc_selected_date()

    render_calendar_with_records()

    if today_records:
        df = pd.DataFrame(today_records)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records yet.")
