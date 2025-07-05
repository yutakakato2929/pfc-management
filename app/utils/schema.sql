-- schema.sql
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    amount REAL NOT NULL,
    kcal REAL NOT NULL,
    protein REAL NOT NULL,
    fat REAL NOT NULL,
    carb REAL NOT NULL,
    note TEXT,
    user_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS consumption_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    kcal REAL NOT NULL,
    protein REAL NOT NULL,
    fat REAL NOT NULL,
    carb REAL NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);