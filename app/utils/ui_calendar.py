import calendar
from datetime import datetime, date
import streamlit.components.v1 as components

def render_calendar_with_records(records_by_date):
    today = date.today()
    year, month = today.year, today.month

    # 日付 → カロリー合計 に変換
    calories_per_day = {}
    for d, records in records_by_date.items():
        if d.startswith(f"{year}-{str(month).zfill(2)}"):
            total_kcal = sum(r["kcal"] for r in records)
            day = int(d.split("-")[2])
            calories_per_day[day] = total_kcal

    # カレンダー作成
    cal = calendar.Calendar(firstweekday=6)  # 0=月曜, 6=日曜
    month_days = cal.monthdayscalendar(year, month)

    # CSS＋HTMLで整える
    html = """
    <style>
    body {
        font-family: 'Helvetica Neue', sans-serif;
        color: #555;
    }

    table.calendar {
        background-color:#555;
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        margin-top: 1em;
        padding: 0 5px;
    }

    .calendar th {
        color: #ccc;
        font-size: 14px;
        padding: 8px;
    }

    .calendar td {
        background-color: #ccc;
        color: #fff;
        border-radius: 8px;
        height: 80px;
        vertical-align: top;
        padding: 6px;
        position: relative;
    }

    .calendar .marked {
        background-color: #69cbdb;
        border: 2px solid #b3f7ff;
        font-weight: bold;
        color: #fff;
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
    components.html(html, height=620)