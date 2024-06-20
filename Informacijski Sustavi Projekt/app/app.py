from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

# Initialize the Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize MySQL connection
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

# Create Task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO tasks (title, description) VALUES (%s, %s)', (title, description))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Read Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    return jsonify(tasks)

# Update Task
@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']
    description = request.form['description']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE tasks SET title = %s, description = %s WHERE id = %s', (title, description, id))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Delete Task
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
