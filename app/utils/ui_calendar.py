import calendar
import streamlit as st
import streamlit.components.v1 as components

def render_calendar_with_records():
    target_day = st.session_state.date_input
    year, month = target_day.year, target_day.month

    calories_per_day = {}
    for record in st.session_state.consumption_records:
        record_date = record["date"]
        if record_date.startswith(f"{year}-{str(month).zfill(2)}"):
            day = int(record_date.split("-")[2])
            calories_per_day[day] = calories_per_day.get(day, 0) + record["kcal"]

    # カレンダー作成
    cal = calendar.Calendar(firstweekday=6)  # 0=月曜, 6=日曜
    month_days = cal.monthdayscalendar(year, month)

    # CSS＋HTMLで整える
    html = """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        color: #333;
    }

    table.calendar {
        width: 100%;
        border-collapse: separate; /* セル間の隙間を有効にする */
        margin: 1em 0;
        border-radius: 6px; /* カレンダー全体の丸み */
        overflow: hidden; /* 丸みを適用 */
    }

    .calendar th {
        background-color: #f4f4f4;
        color: #333;
        font-size: 14px;
        padding: 5px;
        text-align: center;
        border-radius: 6px; /* ヘッダーセルの丸み */
        border: 1px solid #ddd;
    }

    .calendar td {
        background-color: #fff;
        color: #333;
        border: 1px solid #ddd;
        border-radius: 6px; /* 各セルの丸み */
        height: 80px;
        vertical-align: top;
        padding: 6px;
        position: relative;
        # box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 軽い影を追加 */
    }

    .calendar .marked {
        background-color: #69cbdb;
        border: 2px solid #b3f7ff;
        font-weight: bold;
        color: #fff;
        border-radius: 6px; /* マークされたセルの丸み */
    }

    .calendar .day-num {
        font-size: 16px;
        font-weight: bold;
        position: absolute;
        top: 6px;
        left: 6px;
    }

    .calendar .kcal {
        font-size: 12px;
        position: absolute;
        bottom: 6px;
        right: 6px;
        color: #fff;
    }
    </style>
    """

    # カレンダーの高さを週数に応じて調整
    num_weeks = len(month_days)
    table_height = 80 * num_weeks + 230

    html += f"<h1>{year}年 {month}月</h3><table class='calendar'>"

    weekdays = ["日", "月", "火", "水", "木", "金", "土",]
    html += "<tr>" + "".join(f"<th>{w}</th>" for w in weekdays) + "</tr>"

    for week in month_days:
        html += "<tr>"
        for day in week:
            if day == 0:
                html += "<td></td>"
            else:
                if day in calories_per_day:
                    kcal = calories_per_day[day]
                    html += f"<td class='marked'><div class='day-num'>{day}</div><span class='kcal'>{kcal:.0f} kcal</span></td>"
                else:
                    html += f"<td><div class='day-num'>{day}</div></td>"
        html += "</tr>"

    html += "</table>"
    components.html(html, height=table_height)
