from flask import jsonify, request

USERS = {
    "admin": "admin123",
    "user": "user123",
}

def register_auth(app):

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"error": "Укажите username и password"}), 400

        username = data.get('username')
        password = data.get('password')

        if USERS.get(username) != password:
            return jsonify({"error": "Неверный логин или пароль"}), 401

        return jsonify({
            "message": "Успешная авторизация",
            "user": username
        }), 200

    @app.route('/logout', methods=['POST'])
    def logout():
        return jsonify({"message": "Выход выполнен"}), 200