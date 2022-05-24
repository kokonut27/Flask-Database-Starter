import sqlite3 

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, username, userid, content, topic, likes) VALUES (?, ?, ?, ?, ?, ?)", ('The first post ever!', 'JBloves27', 3282411, 'Wowzas, its the first post to ever live on GlitchMedia!!! ', 'fun', 0))

connection.commit()
connection.close()