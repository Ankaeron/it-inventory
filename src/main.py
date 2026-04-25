from flask import Flask, jsonify
from inventory import register_routes
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sqlite')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                type       TEXT,
                serial     TEXT    UNIQUE,
                status     TEXT    DEFAULT 'В работе',
                department TEXT,
                created_at TEXT    DEFAULT (datetime('now', 'localtime'))
            )
        ''')
        conn.commit()

init_db()
register_routes(app)  # подключаем маршруты из inventory.py


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sqlite')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                type       TEXT,
                serial     TEXT    UNIQUE,
                status     TEXT    DEFAULT 'В работе',
                department TEXT,
                created_at TEXT    DEFAULT (datetime('now', 'localtime'))
            )
        ''')
        conn.commit()

init_db()


@app.route('/')
def index():
<<<<<<< HEAD
    return jsonify({
        "app": "Система учёта компьютерной техники",
        "version": "1.0.0",
        "status": "ok"
=======
    with get_db() as conn:
        total = conn.execute('SELECT COUNT(*) FROM inventory').fetchone()[0]
        in_use = conn.execute("SELECT COUNT(*) FROM inventory WHERE status = 'В работе'").fetchone()[0]
        on_repair = conn.execute("SELECT COUNT(*) FROM inventory WHERE status = 'На ремонте'").fetchone()[0]
    return jsonify({
        "app": "Система учёта компьютерной техники",
        "version": "1.0.0",
        "stats": {
            "total": total,
            "in_use": in_use,
            "on_repair": on_repair,
            "other": total - in_use - on_repair,
        }
>>>>>>> feature/inventory-module
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Маршрут не найден"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == '__main__':
    app.run(debug=False)