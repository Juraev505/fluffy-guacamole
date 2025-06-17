import sqlite3


conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    grade TEXT
)
''')
conn.commit()


cursor.execute('SELECT COUNT(*) FROM students')
if cursor.fetchone()[0] == 0:
    students_data = [
        ('Alice', 20, 'A'),
        ('Bob', 22, 'B'),
        ('Charlie', 19, 'C'),
        ('Diana', 21, 'B+')
    ]
    cursor.executemany('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', students_data)
    conn.commit()
