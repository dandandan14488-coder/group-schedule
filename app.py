
import os
import sqlite3
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "schedule.db")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key-in-production"
)

ALLOWED_GROUP = "БҚ 24-3"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash(
                "Кестені көру үшін жүйеге кіріңіз.",
                "warning"
            )
            return redirect(url_for("login"))

        return view_function(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("schedule"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        group_name = request.form.get(
            "group_name",
            ALLOWED_GROUP
        ).strip()

        if not username or not password:
            flash(
                "Логин мен парольді толтырыңыз.",
                "danger"
            )
            return render_template("register.html")

        if len(password) < 6:
            flash(
                "Пароль кемінде 6 таңбадан тұруы керек.",
                "danger"
            )
            return render_template("register.html")

        if group_name != ALLOWED_GROUP:
            flash(
                f"Бұл нұсқада тек {ALLOWED_GROUP} тобы қолданылады.",
                "danger"
            )
            return render_template("register.html")

        connection = get_db_connection()

        existing_user = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user is not None:
            connection.close()

            flash(
                "Бұл логин бұрын тіркелген.",
                "danger"
            )
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        connection.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                group_name
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                password_hash,
                group_name
            )
        )

        connection.commit()
        connection.close()

        flash(
            "Тіркелу сәтті аяқталды. Енді жүйеге кіріңіз.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if (
            user is None
            or not check_password_hash(
                user["password_hash"],
                password
            )
        ):
            flash(
                "Логин немесе пароль қате.",
                "danger"
            )
            return render_template("login.html")

        session.clear()

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["group_name"] = user["group_name"]

        return redirect(url_for("schedule"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()

    flash(
        "Жүйеден шықтыңыз.",
        "success"
    )

    return redirect(url_for("login"))


@app.route("/schedule")
@login_required
def schedule():
    group_name = session["group_name"]

    connection = get_db_connection()

    lessons = connection.execute(
        """
        SELECT
            weekday,
            lesson_number,
            time_start,
            time_end,
            subject,
            teacher,
            room
        FROM schedule
        WHERE group_name = ?
        ORDER BY
            CASE weekday
                WHEN 'Дүйсенбі' THEN 1
                WHEN 'Сейсенбі' THEN 2
                WHEN 'Сәрсенбі' THEN 3
                WHEN 'Бейсенбі' THEN 4
                WHEN 'Жұма' THEN 5
                WHEN 'Сенбі' THEN 6
                ELSE 7
            END,
            lesson_number
        """,
        (group_name,)
    ).fetchall()

    connection.close()

    return render_template(
        "schedule.html",
        lessons=lessons,
        group_name=group_name
    )


if __name__ == "__main__":
    app.run(debug=True)