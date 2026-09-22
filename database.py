import sqlite3


def init_db():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            group_name TEXT NOT NULL
        )
    ''')

    # Создание таблицы расписания
    cursor.execute('''
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
    ''')

    # Очистка старых данных и добавление тестового расписания
    cursor.execute('DELETE FROM schedule')
    dummy_schedule = [
        ('ИС-21', 'Понедельник', 1, 'Проектирование ПО', 'Иванов И.И.', 'Ауд. 404', '09:00', '10:30'),
        ('ИС-21', 'Понедельник', 2, 'Базы данных', 'Петров П.П.', 'Ауд. 405', '10:40', '12:10'),
        ('ИС-21', 'Вторник', 1, 'Веб-разработка', 'Сидоров С.С.', 'Ауд. 312', '09:00', '10:30'),
        ('ПИ-22', 'Понедельник', 1, 'Высшая математика', 'Смирнов А.А.', 'Ауд. 101', '09:00', '10:30')
    ]

    cursor.executemany('''
        INSERT INTO schedule (group_name, weekday, lesson_number, subject, teacher, room, time_start, time_end)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', dummy_schedule)

    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена тестовыми данными.")


if __name__ == '__main__':
    init_db()