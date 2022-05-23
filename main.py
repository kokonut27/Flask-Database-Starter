# Social Media Database (With login system using Replit's db)

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

app = flask.Flask(__name__,
                  static_url_path='',
                  static_folder='static',
                  template_folder='templates')
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

try:
  if db["topics"]:
    print("db key 'topics' exists")
  else:
    db["topics"] = []
except:
  db["topics"] = []

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
      user_id = flask.request.headers['X-Replit-User-Id']
    )

@app.route('/posts', methods = ["POST", "GET"])
def posts():
  conn = get_db_connection()
  posts = conn.execute('SELECT * FROM posts').fetchall()
  conn.close()
  return flask.render_template(
    'posts.html',
    username = flask.request.headers['X-Replit-User-Name'],
    posts = list(reversed(posts))
  )

@app.route('/posts/<int:post_id>')
def post(post_id):
  post = get_post(post_id)
  db["topics"].append(post['topic'])
  return flask.render_template(
    'post.html',
    post = post,
    content = markdown2.markdown(post["content"]),
    username = flask.request.headers['X-Replit-User-Name']
  )

@app.route('/create', methods = ["POST", "GET"])
def create():
  pass

if __name__ == "__main__":
  app.run(port = 8080, host = "0.0.0.0")