import sqlite3 

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, topic) VALUES (?, ?, ?)", ('The first post!', 'Content for the first post', 'coding'))

connection.commit()
connection.close()