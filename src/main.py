from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Система учёта компьютерной техники</h1><p>Добро пожаловать!</p>'

@app.route('/equipment')
def equipment():
    return '<h2>Список оборудования</h2><p>Здесь будет список всей техники организации.</p>'

@app.route('/equipment/<int:item_id>')
def equipment_detail(item_id):
    return f'<h2>Оборудование #{item_id}</h2><p>Подробная информация об единице техники.</p>'

if __name__ == '__main__':
    app.run(debug=False)