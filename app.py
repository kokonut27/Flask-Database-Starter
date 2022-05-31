import flask
import sqlite3
import markdown2
import os
from replit import db
from werkzeug.exceptions import abort

def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn

def get_post(post_id):
  conn = get_db_connection()
  post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id, )).fetchone()
  conn.close()
  if post == None:
    abort(404)
  return post

def get_user(user_id):
  conn = get_db_connection()
  user = conn.execute('SELECT * FROM userInfo WHERE userNum = ?', (user_id, )).fetchone()
  conn.close()
  if user == None:
    abort(404)
  return user

app = flask.Flask(__name__,
                  static_url_path='',
                  static_folder='static',
                  template_folder='templates')
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
topics = ['fun', 'coding', 'gaming', 'random']

# db.clear()

try:
  if db[os.environ["REPL_OWNER"]]:
    print("db key", os.environ["REPL_OWNER"], "exists")
  else:
    db[os.environ["REPL_OWNER"]] = {}
  if db[os.environ["REPL_OWNER"]]["topics"]:
    print("db key 'topics' exists")
  else:
    db[os.environ["REPL_OWNER"]]["topics"] = []
  if db[os.environ["REPL_OWNER"]]["hasLiked"]:
    print("db key 'hasLiked' exists")
  else:
    db[os.environ["REPL_OWNER"]]["hasLiked"] = []
except:
  db[os.environ["REPL_OWNER"]] = {}
  db[os.environ["REPL_OWNER"]]["topics"] = []
  db[os.environ["REPL_OWNER"]]["hasLiked"] = []

@app.route('/')
def index():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  conn.close()
  return flask.render_template(
    'index.html',
    loggedIn = flask.request.headers['X-Replit-User-Id'],
    posts = posts
  )

@app.route('/login', methods = ["POST", "GET"])
def login():
  if flask.request.method == "POST":
    loggedIn = flask.request.headers['X-Replit-User-Id']
    username = flask.request.headers['X-Replit-User-Name']
    conn = get_db_connection()
    conn.execute("INSERT INTO userInfo (username, userid) VALUES (?, ?)", (username, loggedIn))
    conn.commit()
    conn.close()
    return flask.render_template(
      'login.html',
      loggedIn = loggedIn
    )

  if flask.request.method == "GET":
    return flask.render_template('login.html')

@app.route('/dashboard', methods = ["POST", "GET"])
def dashboard():
  if flask.request.method == "GET":
    return flask.render_template(
      'dashboard.html',
      username = flask.request.headers['X-Replit-User-Name'],
      user_id = flask.request.headers['X-Replit-User-Id'],
      loggedIn = flask.request.headers['X-Replit-User-Id']
    )

@app.route('/posts', methods = ["POST", "GET"])
def posts():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  conn.close()
  return flask.render_template(
    'posts.html',
    username = flask.request.headers['X-Replit-User-Name'],
    posts = list(reversed(posts)),
    loggedIn = flask.request.headers['X-Replit-User-Id']
  )

@app.route('/posts/<int:post_id>')
def post(post_id):
  post = get_post(post_id)
  db[os.environ["REPL_OWNER"]]["topics"].append(post['topic'])
  return flask.render_template(
    'post.html',
    post = post,
    content = markdown2.markdown(post["content"]),
    username = flask.request.headers['X-Replit-User-Name'],
    loggedIn = flask.request.headers['X-Replit-User-Id']
  )

@app.route('/create', methods = ["POST", "GET"])
def create():
  username = flask.request.headers['X-Replit-User-Name']
  userId = flask.request.headers['X-Replit-User-Id']
  if flask.request.method == "POST":
    title = flask.request.form['title']
    content = flask.request.form['content']
    topic = flask.request.form['topic']

    if topic not in topics:
      flask.flash('No such topic exists!')
    else:
      if not title:
        flask.flash('The title is required!')
      else:
        conn = get_db_connection()
        conn.execute("INSERT INTO posts (title, content, username, topic, userid, likes) VALUES (?, ?, ?, ?, ?, ?)", (title, content, username, topic, userId, 0))
        conn.commit()
        conn.close()
        return flask.redirect(flask.url_for('index'))
  return flask.render_template('create.html')

@app.route('/edit/<int:post_id>')
def edit(post_id):
  post = get_post(post_id)

@app.route('/like/<int:post_id>', methods = ["POST", "GET"])
def like(post_id):
  get_post(post_id) # check if post exists :D
  userHasLiked = db[os.environ["REPL_OWNER"]]["hasLiked"]
  for posts in userHasLiked:
    if post_id == posts:
      conn = get_db_connection()
      conn.execute("UPDATE posts SET likes = likes - 1")
      conn.commit()
      conn.close()
      db[os.environ["REPL_OWNER"]]["hasLiked"].remove(post_id)
    else:
      conn = get_db_connection()
      conn.execute("UPDATE posts SET likes = likes + 1")
      conn.commit()
      conn.close()
      db[os.environ["REPL_OWNER"]]["hasLiked"].append(post_id)
  return flask.redirect(flask.url_for('posts'))

@app.route('/user/<int:user_id>')
def user(user_id):
  get_user(user_id)
  return flask.render_template(
    'user.html',
    user_id = user_id,
    username = flask.request.headers['X-Replit-User-Name'],
    loggedIn = flask.request.headers['X-Replit-User-Id']
  )