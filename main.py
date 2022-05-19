# Social Media Database Template (With login system using Replit's db)

import flask
import sqlite3
import markdown2
import os
from replit import db

app = flask.Flask(__name__,
                  static_url_path='',
                  static_folder='static',
                  template_folder='templates')
try:
  if not db["loggedIn"]:
    print("loggedIn databbase key has been made.")
except:
  db["loggedIn"] = True



@app.route('/')
def index():
  return flask.render_template(
    'index.html',
    loggedIn = db["loggedIn"]
  )

@app.route('/signup', methods = ["POST", "GET"])
def signup():
  if flask.request.method == "POST":
    username = flask.request.form['signupUsername']
    password = flask.request.form['signupPassword']
    if db[username]:
      flask.flash('That username already exists!')
      return flask.redirect(flask.url_for('/signup'))
    else:
      db[username] = password
      return flask.redirect(flask.url_for('/dashboard'))

  if flask.request.method == "GET":
    return flask.render_template('signup.html')

app.run(port = 8080, host = "0.0.0.0")