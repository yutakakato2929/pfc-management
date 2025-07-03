import streamlit as st
import pandas as pd
from datetime import datetime

st.title("統計")

records_by_date = st.session_state.get("records_by_date", {})

if not records_by_date:
    st.info("まだデータがありません。")
else:
    # 日別にPFC合計を計算
    summary = []
    for date, records in records_by_date.items():
        kcal = sum(r["kcal"] for r in records)
        p = sum(r["protein"] for r in records)
        f = sum(r["fat"] for r in records)
        c = sum(r["carb"] for r in records)
        summary.append({"date": date, "kcal": kcal, "P": p, "F": f, "C": c})

    df = pd.DataFrame(summary).sort_values("date", ascending=False)
    st.dataframe(df, use_container_width=True)

    st.line_chart(df.set_index("date")[["P", "F", "C"]])