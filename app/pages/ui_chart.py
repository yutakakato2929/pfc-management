import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import get_today_records

st.title("統計")

today_records = get_today_records()

if not today_records:
    st.info("まだデータがありません。")
else:
    # 日別にPFC合計を計算
    kcal, p, f, c = 0, 0, 0, 0
    summary = []
    for record in today_records:
        kcal += record["kcal"]
        p += record["protein"]
        f += record["fat"]
        c += record["carb"]
    summary.append({"date": "ちょっとたいむ", "kcal": kcal, "P": p, "F": f, "C": c})

    df = pd.DataFrame(summary).sort_values("date", ascending=False)
    st.dataframe(df, use_container_width=True)

    st.line_chart(df.set_index("date")[["P", "F", "C"]])