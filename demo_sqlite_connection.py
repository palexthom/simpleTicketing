import sqlite3

conn = sqlite3.connect('databases/ticketing.db')
c = conn.cursor()

c.execute('SELECT * FROM users')
truc = c.fetchone()
for t in truc:
    print(t)