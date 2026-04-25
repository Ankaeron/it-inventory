from flask import jsonify, request
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sqlite')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def register_routes(app):

    @app.route('/inventory', methods=['GET'])
    def get_all():
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM inventory').fetchall()
        return jsonify([dict(r) for r in rows])

    @app.route('/inventory/<int:item_id>', methods=['GET'])
    def get_one(item_id):
        with get_db() as conn:
            row = conn.execute('SELECT * FROM inventory WHERE id = ?', (item_id,)).fetchone()
        if row is None:
            return jsonify({"error": "Оборудование не найдено"}), 404
        return jsonify(dict(row))

    @app.route('/inventory', methods=['POST'])
    def create():
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({"error": "Поле name обязательно"}), 400
        try:
            with get_db() as conn:
                cursor = conn.execute(
                    'INSERT INTO inventory (name, type, serial, status, department) VALUES (?, ?, ?, ?, ?)',
                    (data.get('name'), data.get('type', ''), data.get('serial', ''),
                     data.get('status', 'В работе'), data.get('department', ''))
                )
                conn.commit()
                row = conn.execute('SELECT * FROM inventory WHERE id = ?', (cursor.lastrowid,)).fetchone()
            return jsonify(dict(row)), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Серийный номер уже существует"}), 409

    @app.route('/inventory/<int:item_id>', methods=['PUT'])
    def update(item_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Нет данных для обновления"}), 400
        allowed = {'name', 'type', 'serial', 'status', 'department'}
        fields = {k: v for k, v in data.items() if k in allowed}
        if not fields:
            return jsonify({"error": "Нет допустимых полей для обновления"}), 400
        set_clause = ', '.join(f'{k} = ?' for k in fields)
        values = list(fields.values()) + [item_id]
        with get_db() as conn:
            cursor = conn.execute(f'UPDATE inventory SET {set_clause} WHERE id = ?', values)
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Оборудование не найдено"}), 404
            row = conn.execute('SELECT * FROM inventory WHERE id = ?', (item_id,)).fetchone()
        return jsonify(dict(row))

    @app.route('/inventory/<int:item_id>', methods=['DELETE'])
    def delete(item_id):
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
            conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Оборудование не найдено"}), 404
        return jsonify({"message": f"Оборудование #{item_id} удалено"}), 200