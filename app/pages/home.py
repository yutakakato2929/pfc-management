import streamlit as st
import pandas as pd
from utils.helpers import get_records_by_date, get_totals, get_today_str
from utils.ui_calendar import render_calendar_with_records

today_str = get_today_str()
today_records = get_records_by_date(today_str)
kcal, p, f, c = get_totals(today_records)

with st.container():
    st.title("PFC MANAGEMENT")

    render_calendar_with_records(today_records)

    st.subheader("WHAT YOU ATE TODAY") 
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("カロリー", f"{kcal:.0f} kcal")
    col2.metric("P（たんぱく質）", f"{p:.1f} g")
    col3.metric("F（脂質）", f"{f:.1f} g")
    col4.metric("C（炭水化物）", f"{c:.1f} g")

    if today_records:
        df = pd.DataFrame(today_records)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records yet.")
