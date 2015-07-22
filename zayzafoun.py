# -*- coding: utf-8 -*-
# all the imports
import sqlite3
# import bleach
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, current_app
from contextlib import closing

# configuration
WEBSITENAME = "زيزفون"
DATABASE = 'zayzafoun.db'
DEBUG = False
SECRET_KEY = 'EVAQZHWCMWEJWHTOPPOIEWMCOIGWJGJWEXZOKWMTP'
USERNAME = 'admin'
PASSWORD = 'default'
DISQUSNAME = "zayzafoun"


# Creating the application.
app = Flask(__name__)
app.config.from_object(__name__)

## You can uncomment this section if you want to run bleach to clean the code.
## Right now, it does nothing.
#tags = ['b', 'p', 'strong', 'pre', 'code', 'img', 'ul', 'li', 'i', 'a', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'table', 'tr', 'td', 'div', 'span', 'font', 'video']
#attributes = {
#    'a': ['href', 'rel'],
#    'img': ['src', 'alt'],
#    'div': ['align', 'style', 'class'],
#    'font': ['face', 'color', 'size'],
#    'span': ['style']
#}

def cleanCode(text):
  ## Don't forget to remove the comment here too, and call me pro.
  #newtext = bleach.clean(text, tags=tags, attributes=attributes)
  return text

@app.context_processor
def variables_def():
  return dict(websiteName=unicode(WEBSITENAME, "utf-8"), disqusName=DISQUSNAME, currentUrl=request.path, cleanCode=cleanCode)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])


def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()


def get_pages():
  fetch_pages = g.db.execute('select * from pages order by pageid')
  pages = [dict(pageid=y[0], pageurl=y[1], pagetitle=y[2]) for y in fetch_pages.fetchall()]
  return pages


def get_posts():
  posts = ""
  fetch_posts = g.db.execute('select * from posts order by postid desc')
  posts = [dict(postid=x[0], posttitle=x[1], posturl=x[2], postcontent=x[
                3], postauthor=x[4], postdate=x[5]) for x in fetch_posts.fetchall()]
  return posts


def single_post(posturl):
  showingpost = g.db.execute(
      'select * from posts where posturl = ?', (posturl,))
  for x in showingpost.fetchall():
    postid, posttitle, posturl, postcontent, postauthor, postdate = x[
        0], x[1], x[2], x[3], x[4], x[5]
  post = [postid, posttitle, posturl, postcontent, postauthor, postdate]
  return post

def editpost(posturl):
    getPost = g.db.execute('select * from posts where posturl = ?', (posturl,))
    for n in getPost.fetchall():
      posttitle, posturl, postcontent, = n[1], n[2], n[3]
    post = [posttitle, posturl, postcontent]
    return post

def single_page(pageurl):
  showingpage = g.db.execute('select * from pages where pageurl= ?', (pageurl,))
  for x in showingpage.fetchall():
    pageid, pageurl, pagetitle, pagecontent, pageauthor, pagedate = x[0], x[1], x[2], x[3], x[4], x[5]
  page = [pageid, pageurl, pagetitle, pagecontent, pageauthor, pagedate]
  return page

def editpage(pageurl):
    getPage = g.db.execute('select * from pages where pageurl = ?', (pageurl,))
    for n in getPage.fetchall():
      pagetitle, pageurl, pagecontent, = n[1], n[2], n[3]
    page = [pageurl, pagetitle, pagecontent]
    return page

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


@app.route('/')
def show_index():
  return render_template('index.html', posts=get_posts(), pages=get_pages())

@app.route('/<posturl>')
def show_post(posturl):
  return render_template('post.html', post=single_post(posturl), posts=get_posts(), pages=get_pages())

@app.route('/<posturl>/edit')
def postedit(posturl):
  return render_template('edit.html', post = editpost(posturl), contentType = "post", pages=get_pages())

@app.route('/<posturl>/delete')
def postdelete(posturl):
    g.db.execute('delete from posts where posturl = ? limit 1', (posturl,))
    g.db.commit()
    return render_template('index.html', posts=get_posts(), pages=get_pages())

@app.route('/page/<pageurl>')
def show_page(pageurl):
  return render_template('page.html', page=single_page(pageurl), pages=get_pages())

@app.route('/page/<pageurl>/edit')
def pageedit(pageurl):
    return render_template('edit.html', post = editpage(pageurl), contentType = "page", pages=get_pages())

@app.route('/page/<pageurl>/delete')
def pagedelete(pageurl):
      g.db.execute('delete from pages where pageurl = ? limit 1', (pageurl,))
      g.db.commit()
      return render_template('index.html', posts=get_posts(), pages=get_pages())

@app.route('/archive')
def archive():
      return render_template('archive.html', posts=get_posts(), pages=get_pages())

@app.route('/publish', methods=['GET', 'POST'])
def publish():
  if request.method == 'POST':
    if request.form["contenttype"] == "post":
      g.db.execute('insert into posts (posttitle, posturl, postcontent, postauthor) values (?, ?, ?, ?)',
                   (request.form['title'], request.form['url'], request.form['content'], session['username']))
      g.db.commit()
      return redirect(url_for('show_index'))
    else:
      g.db.execute('insert into pages (pagetitle, pageurl, pagecontent, pageauthor) values (?, ?, ?, ?)',
                   (request.form['title'], request.form['url'], request.form['content'], session['username']))
      g.db.commit()
      return redirect(url_for('show_index'))
  elif request.method == 'GET':
    return render_template('new.html', pages=get_pages())

@app.route('/publishedit', methods=['POST'])
def doEdit():
  if request.method == 'POST':
    if request.form["contenttype"] == "post":
      g.db.execute('UPDATE posts SET posttitle = ?, postcontent = ? WHERE posturl = ?', (request.form['title'], request.form['content'], request.form['url']))
      g.db.commit()
      return redirect(url_for('show_index'))
    else:
      g.db.execute('UPDATE pages SET pagetitle = ?, pagecontent = ? WHERE pageurl = ?', (request.form['title'], request.form['content'], request.form['url']))
      g.db.commit()
      return redirect(url_for('show_index'))
  else:
      return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      session['username'] = app.config['USERNAME']
      return redirect(url_for('show_index'))
  return render_template('login.html', pages=get_pages())


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  return redirect(url_for('show_index'))

if __name__ == "__main__":
  init_db()
  app.run()
