from flask import Flask, jsonify
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


@app.route('/')
def index():
    return jsonify({
        "app": "Система учёта компьютерной техники",
        "version": "1.0.0",
        "status": "ok"
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Маршрут не найден"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == '__main__':
    app.run(debug=False)