import sqlite3
from pathlib import Path

# PATH設定
DB_PATH = Path(__file__).parent.parent / "data" / "app.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

# DBに接続（存在しなければ自動生成）
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# テーブル初期化
def init_db():
    with get_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()

# データ挿入
def insert_ingredient(row: dict):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ingredients
                    (name, unit, amount, kcal, protein, fat, carb, note)
            VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["name"],
            row["unit"],
            row["amount"],
            row["kcal"],
            row["protein"],
            row["fat"],
            row["carb"],
            row.get("note", "")
        ))
        conn.commit()
        return cur.lastrowid  # ← 挿入した行のidを返す

def insert_consumption(row: dict):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO consumption_records 
                    (date, ingredient_id, quantity, kcal, protein, fat, carb)
            VALUES
                    (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["date"],
            row["ingredient_id"],
            row["quantity"],
            row["kcal"],
            row["protein"],
            row["fat"],
            row["carb"],
        ))
        conn.commit()
        return cur.lastrowid  # ← 挿入した行のidを返す

# データ取得
def select_all_ingredients():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ingredients")
        rows = cur.fetchall()
        return [dict(row) for row in rows] 
    
def select_records_by_date(date_str: str):
    with get_connection() as conn:
        cur = conn.cursor()
        query = """
        SELECT
            cr.id,
            cr.date,
            cr.ingredient_id,
            ing.name,
            ing.unit,
            cr.quantity,
            cr.kcal,
            cr.protein,
            cr.fat,
            cr.carb
        FROM consumption_records cr
        JOIN ingredients ing ON cr.ingredient_id = ing.id
        WHERE cr.date = ?
        ORDER BY cr.id ASC
        """
        cur.execute(query, (date_str,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]