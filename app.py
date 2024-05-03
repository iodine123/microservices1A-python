from flask import Flask, render_template, request, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import os
import logging

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(filename='/app/logs.log', level=logging.INFO)

db_name = os.environ.get('POSTGRES_DB', 'todo_db')
db_user = os.environ.get('POSTGRES_USER', 'root_toor')
db_password = os.environ.get('POSTGRES_PASSWORD', 'password')
db_host = os.environ.get('POSTGRES_HOST', 'postgresql-service')  
db_port = os.environ.get('POSTGRES_PORT', '5432')

# Function to create database and table
def create_table():
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id SERIAL PRIMARY KEY, task TEXT)''')
    conn.commit()
    conn.close()

# Home route to display tasks
@app.route('/')
def home():
    create_table()
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
