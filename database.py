
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "schedule.db")

GROUP_NAME = "БҚ 24-3"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            group_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            weekday TEXT NOT NULL,
            lesson_number INTEGER NOT NULL,
            subject TEXT NOT NULL,
            teacher TEXT NOT NULL,
            room TEXT NOT NULL,
            time_start TEXT NOT NULL,
            time_end TEXT NOT NULL
        )
    """)

    # БҚ 24-3 тобының бұрынғы сабақтарын өшіру
    cursor.execute(
        "DELETE FROM schedule WHERE group_name = ?",
        (GROUP_NAME,)
    )

    # БҚ 24-3 тобының апталық сабақ кестесі
    lessons = [
        # ДҮЙСЕНБІ
        (
            GROUP_NAME, "Дүйсенбі", 1,
            "КМ 04 ОН 4.3 Бағдарламалық қамтамасыздандыруды жобалау",
            "Закарина Н.Қ.", "315", "11:55", "13:25"
        ),
        (
            GROUP_NAME, "Дүйсенбі", 2,
            "КМ 04 ОН 4.2 Бағдарламалық қамтамасыздандыруды жобалау",
            "Нұрекешов Д.С.", "316", "13:35", "15:05"
        ),
        (
            GROUP_NAME, "Дүйсенбі", 3,
            "КМ 04 ОН 4.1 Бағдарламалық қамтамасыздандыруды жобалау",
            "Пилтан Н.Қ.", "313", "15:15", "16:45"
        ),
        (
            GROUP_NAME, "Дүйсенбі", 4,
            "КМ 04 ОН 4.1 Бағдарламалық қамтамасыздандыруды жобалау",
            "Пилтан Н.Қ.", "313", "17:00", "18:25"
        ),

        # СЕЙСЕНБІ
        (
            GROUP_NAME, "Сейсенбі", 1,
            "КМ 04 ОН 4.2 Бағдарламалық қамтамасыздандыруды жобалау",
            "Нұрекешов Д.С.", "316", "11:55", "13:25"
        ),
        (
            GROUP_NAME, "Сейсенбі", 2,
            "КМ 04 ОН 4.4 Бағдарламалық қамтамасыздандыруды жобалау",
            "Орымбеков Ғ.Қ.", "321", "13:35", "15:05"
        ),
        (
            GROUP_NAME, "Сейсенбі", 3,
            "КМ 04 ОН 4.5 Бағдарламалық қамтамасыздандыруды жобалау",
            "Закарина Н.Қ.", "315", "15:15", "16:45"
        ),
        (
            GROUP_NAME, "Сейсенбі", 4,
            "КМ 04 ОН 4.5 Бағдарламалық қамтамасыздандыруды жобалау",
            "Закарина Н.Қ.", "315", "17:00", "18:25"
        ),

        # СӘРСЕНБІ
        (
            GROUP_NAME, "Сәрсенбі", 2,
            "КМ 04 ОН 4.3 Бағдарламалық қамтамасыздандыруды жобалау",
            "Закарина Н.Қ.", "315", "13:35", "15:05"
        ),
        (
            GROUP_NAME, "Сәрсенбі", 3,
            "КМ 04 ОН 4.2 Бағдарламалық қамтамасыздандыруды жобалау",
            "Нұрекешов Д.С.", "316", "15:15", "16:45"
        ),
        (
            GROUP_NAME, "Сәрсенбі", 4,
            "КМ 04 ОН 4.1 Бағдарламалық қамтамасыздандыруды жобалау",
            "Пилтан Н.Қ.", "313", "17:00", "18:25"
        ),

        # БЕЙСЕНБІ
        (
            GROUP_NAME, "Бейсенбі", 1,
            "КМ 04 ОН 4.6 Бағдарламалық қамтамасыздандыруды жобалау",
            "Рзаханов Д.М.", "320", "11:55", "13:25"
        ),
        (
            GROUP_NAME, "Бейсенбі", 2,
            "КМ 04 ОН 4.6 Бағдарламалық қамтамасыздандыруды жобалау",
            "Рзаханов Д.М.", "320", "13:35", "15:05"
        ),
        (
            GROUP_NAME, "Бейсенбі", 3,
            "БМ 01 ОН 1.2 Дене қасиеттерін дамыту және жетілдіру",
            "Сәрсенғали М.Б.", "Спорт зал", "15:15", "16:45"
        ),
        (
            GROUP_NAME, "Бейсенбі", 4,
            "КМ 04 ОН 4.2 Бағдарламалық қамтамасыздандыруды жобалау",
            "Нұрекешов Д.С.", "316", "17:00", "18:25"
        ),

        # ЖҰМА
        (
            GROUP_NAME, "Жұма", 1,
            "БМ 01 ОН 1.1 Дене қасиеттерін дамыту және жетілдіру",
            "Сәрсенғали М.Б.", "Спорт зал", "11:55", "13:25"
        ),
        (
            GROUP_NAME, "Жұма", 2,
            "КМ 04 ОН 4.4 Бағдарламалық қамтамасыздандыруды жобалау",
            "Орымбеков Ғ.Қ.", "321", "13:35", "15:05"
        ),
        (
            GROUP_NAME, "Жұма", 3,
            "КМ 04 ОН 4.3 Бағдарламалық қамтамасыздандыруды жобалау",
            "Закарина Н.Қ.", "315", "15:15", "16:45"
        )
    ]

    cursor.executemany("""
        INSERT INTO schedule (
            group_name,
            weekday,
            lesson_number,
            subject,
            teacher,
            room,
            time_start,
            time_end
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, lessons)

    connection.commit()
    connection.close()

    print("БҚ 24-3 тобының 18 сабағы сәтті енгізілді.")
    print(f"Database: {DATABASE}")


if __name__ == "__main__":
    create_database()