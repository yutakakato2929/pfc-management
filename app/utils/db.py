import sqlite3
from pathlib import Path

# PATH設定
DB_PATH = Path(__file__).parent.parent / "data" / "app.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

# DBに接続（存在しなければ自動生成）
def get_connection():
    # ディレクトリ（data）が存在しなければ作成
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # DBに接続（存在しなければ自動生成）
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
                    (name, unit, amount, kcal, protein, fat, carb, note, user_id)
            VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["name"],
            row["unit"],
            row["amount"],
            row["kcal"],
            row["protein"],
            row["fat"],
            row["carb"],
            row.get("note", ""),
            row["user_id"]
        ))
        conn.commit()
        return cur.lastrowid  # ← 挿入した行のidを返す

def insert_consumption(row: dict):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO consumption_records 
                    (date, ingredient_id, quantity, kcal, protein, fat, carb, user_id)
            VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["date"],
            row["ingredient_id"],
            row["quantity"],
            row["kcal"],
            row["protein"],
            row["fat"],
            row["carb"],
            row["user_id"],
        ))
        conn.commit()
        return cur.lastrowid  # ← 挿入した行のidを返す

# データ取得
def select_all_ingredients(user_id: str = None):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ingredients WHERE user_id = ? ORDER BY id ASC", (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows] 
    
def select_all_records(user_id: str = None):
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
        LEFT JOIN ingredients ing ON cr.ingredient_id = ing.id
        WHERE cr.user_id = ?
        ORDER BY cr.id ASC
        """
        cur.execute(query, (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]

# def select_records_by_date(date_str: str):
#     with get_connection() as conn:
#         cur = conn.cursor()
#         query = """
#         SELECT
#             cr.id,
#             cr.date,
#             cr.ingredient_id,
#             ing.name,
#             ing.unit,
#             cr.quantity,
#             cr.kcal,
#             cr.protein,
#             cr.fat,
#             cr.carb
#         FROM consumption_records cr
#         JOIN ingredients ing ON cr.ingredient_id = ing.id
#         WHERE cr.date = ?
#         ORDER BY cr.id ASC
#         """
#         cur.execute(query, (date_str,))
#         rows = cur.fetchall()
#         return [dict(row) for row in rows]

# データ削除
def delete_ingredient(id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM ingredients WHERE id = ?", (id,))
        conn.commit()

def delete_record(id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM consumption_records WHERE id = ?", (id,))
        conn.commit()

# データ更新
def update_ingredient(id: int, value: dict):
    with get_connection() as conn:
        cur = conn.cursor()

        # 動的にSET句を生成
        columns = ", ".join([f"{k} = ?" for k in value.keys()])
        sql = f"UPDATE ingredients SET {columns} WHERE id = ?"

        # 値 + id を渡す
        params = list(value.values()) + [id]

        cur.execute(sql, params)
        conn.commit()

# データ更新
def update_record(id: int, value: dict):
    with get_connection() as conn:
        cur = conn.cursor()

        # 1. 既存のレコードを取得
        cur.execute("SELECT quantity, kcal, protein, fat, carb FROM consumption_records WHERE id = ?", (id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Record with id {id} not found.")

        old_quantity = row["quantity"]

        # 2. もしquantityが更新されるなら、倍率を計算してPFC・kcalを更新
        if "quantity" in value and old_quantity != 0:
            new_quantity = value["quantity"]
            ratio = new_quantity / old_quantity

            for field in ["kcal", "protein", "fat", "carb"]:
                if field in row and field not in value:
                    value[field] = round(row[field] * ratio, 1)

        # 3. 動的にUPDATE文を構築
        columns = ", ".join([f"{k} = ?" for k in value.keys()])
        sql = f"UPDATE consumption_records SET {columns} WHERE id = ?"
        params = list(value.values()) + [id]

        cur.execute(sql, params)
        conn.commit()