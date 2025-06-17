import sqlite3


connection = sqlite3.connect('delivery.db', check_same_thread=False)
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, number TEXT, location TEXT);')
connection.commit()
def register(tg_id, name, number, location):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (tg_id, name, number, location))
def check_user(tg_id):

        if sql.execute('SELECT * FROM users WHERE tg_id=?', (tg_id,)).fetchone():
            return True
        else:
            return False
