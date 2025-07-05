import streamlit as st
import pandas as pd
import plotly.express as px # type: ignore
from datetime import datetime, timedelta
from utils.helpers import get_user_id

get_user_id()

st.title("統計")

if not st.session_state.consumption_records:
    st.info("まだデータがありません。")
else:
    # データをDataFrameに変換
    # records = pd.DataFrame.from_dict(st.session_state.consumption_records, orient="index")
    records = pd.DataFrame(st.session_state.consumption_records)
    records["date"] = pd.to_datetime(records["date"])

    # タブの作成
    tab1, tab2 = st.tabs(["日別のカロリー・PFC変化", "週・月毎の食材消費量"])

    # タブ1: 日別のカロリー・PFC変化
    with tab1:
        st.subheader("日別のカロリー・PFC変化")
        
        # 期間選択（週単位 or 月単位）
        period = st.radio("期間を選択してください", ["週単位", "月単位"], horizontal=True)
        today = datetime.today()

        if period == "週単位":
            start_date = today - timedelta(days=7)
        else:  # 月単位
            start_date = today - timedelta(days=30)

        filtered_records = records[records["date"] >= start_date]

        # 日付ごとにデータを集計
        aggregated_records = filtered_records.groupby("date").sum().reset_index()

        # グラフの作成
        # グラフの作成
        fig = px.bar(
            aggregated_records,
            x="date",
            y=["protein", "fat", "carb"],
            labels={"value": "量 (g)", "variable": "項目", "date": "日付"},
            title=f"{period}のPFCとカロリー変化",
            barmode="group",
            color_discrete_map={
                "protein": "rgba(255, 99, 132, 0.8)",  # 赤
                "fat": "rgba(255, 206, 86, 0.8)",      # 黄色
                "carb": "rgba(54, 162, 235, 0.8)"      # 青
            }
        )

        # 折れ線グラフ（カロリー）を追加
        fig.add_scatter(
            x=aggregated_records["date"],
            y=aggregated_records["kcal"],
            mode="lines+markers",
            name="カロリー (kcal)",
            line=dict(color="rgba(75, 192, 192, 0.8)"),  # 緑
            yaxis="y2"
        )

        # レイアウトの調整（2つのY軸を設定）
        fig.update_layout(
            yaxis=dict(title="量 (g)"),
            yaxis2=dict(
                title="カロリー (kcal)",
                overlaying="y",
                side="right"
            ),
            xaxis=dict(title="日付"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # グラフを表示
        st.plotly_chart(fig, use_container_width=True)

    # タブ2: 週・月毎の食材消費量
    with tab2:
        st.subheader("週・月毎の食材消費量")
        
        # 期間選択（週単位 or 月単位）
        period = st.radio("期間を選択してください", ["週単位", "月単位"], horizontal=True, key="tab2")
        today = datetime.today()

        if period == "週単位":
            start_date = today - timedelta(days=7)
        else:  # 月単位
            start_date = today - timedelta(days=30)

        filtered_records = records[records["date"] >= start_date]

        # 材料ごとの消費量を積み上げ棒グラフで表示
        fig = px.bar(
            filtered_records,
            x="name",
            y="quantity",
            color="date",
            labels={"quantity": "消費量", "name": "材料", "date": "日付"},
            title=f"{period}の材料ごとの消費量",
            barmode="stack"
        )
        st.plotly_chart(fig, use_container_width=True)