from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # В реальном проекте используйте сложный случайный ключ


def get_db_connection():
    conn = sqlite3.connect('schedule.db')
    conn.row_factory = sqlite3.Row
    return conn


# Декоратор для защиты страницы расписания
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return redirect(url_for('schedule'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        group_name = request.form['group_name']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password_hash, group_name) VALUES (?, ?, ?)',
                         (username, generate_password_hash(password), group_name))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Пользователь с таким логином уже существует.')
        finally:
            conn.close()
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['group_name'] = user['group_name']
            return redirect(url_for('schedule'))
        else:
            flash('Неверный логин или пароль.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/schedule')
@login_required
def schedule():
    group_name = session.get('group_name')
    conn = get_db_connection()
    # Выборка расписания только для группы авторизованного пользователя
    cur = conn.execute('SELECT * FROM schedule WHERE group_name = ? ORDER BY weekday, lesson_number', (group_name,))
    schedule_data = cur.fetchall()
    conn.close()

    # Группировка расписания по дням недели
    grouped_schedule = {}
    for row in schedule_data:
        day = row['weekday']
        if day not in grouped_schedule:
            grouped_schedule[day] = []
        grouped_schedule[day].append(row)

    return render_template('schedule.html', schedule=grouped_schedule, group_name=group_name)


if __name__ == '__main__':
    app.run(debug=True)