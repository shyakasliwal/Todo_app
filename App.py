from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db()
    todos = conn.execute("SELECT * FROM todos").fetchall()
    return jsonify([dict(todo) for todo in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO todos (task) VALUES (?)", (data['task'],))
    conn.commit()
    return jsonify({"message": "Todo added"}), 201

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    return jsonify({"message": "Todo deleted"})

if __name__ == '__main__':
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )''')
    conn.commit()
    app.run(debug=True, port=5000, host='0.0.0.0')
