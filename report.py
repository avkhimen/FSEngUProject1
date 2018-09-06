#!/usr/bin/env python3
# 
# A reporting tool to asnwer some questions

from flask import Flask, request, redirect, url_for

import psycopg2, bleach

DBNAME = "news"

#A list with a single element that stores the value of the current question
POSTS = ["none"]

def get_posts():
  """Connect to the database and execute each query depending on the question"""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  if POSTS[0] == "q1":
    c.execute("""SELECT articles.title, count(*) AS num 
                   FROM articles 
                   JOIN log 
                     ON log.path LIKE '%'||articles.slug||'%' 
               GROUP BY articles.title 
               ORDER BY num 
             DESC LIMIT 3""")
    posts = c.fetchall()
  if POSTS[0] == "q2":
    c.execute(""" SELECT DISTINCT totalcount.authorname, sum(totalcount.articlecount) AS totalarticles 
                             FROM (
                                   SELECT count(log.time) AS articlecount, authors.name AS authorname 
                                     FROM articles 
                                     JOIN log 
                                       ON log.path LIKE '%'||articles.slug||'%' 
                                     JOIN authors 
                                       ON authors.id = articles.author 
                                 GROUP BY articles.slug, articles.author, authors.name) AS totalcount 
                         GROUP BY totalcount.authorname 
                         ORDER BY totalarticles DESC""")
    posts = c.fetchall()
  if POSTS[0] == "q3":
    c.execute("""SELECT T3.days 
                   FROM (
                         SELECT T1.days AS days, ROUND(100*T1.badreqs/T2.totalreqs,2) AS percent 
                   FROM (
                         SELECT distinctdays.days AS days, count(log.time) AS badreqs 
                   FROM log 
                   JOIN (
                         SELECT DISTINCT date(log.time) AS days 
                                    FROM log) AS distinctdays 
                     ON date(log.time) = distinctdays.days 
                  WHERE log.status LIKE '%404%' 
               GROUP BY distinctdays.days) AS T1 
                   JOIN (
                        SELECT distinctdays.days AS days, count(log.time) AS totalreqs 
                   FROM log 
                   JOIN (
                        SELECT DISTINCT date(log.time) AS days 
                                   FROM log) AS distinctdays 
                                     ON date(log.time) = distinctdays.days 
                               GROUP BY distinctdays.days) AS T2 
                                     ON T1.days = T2.days 
                               ORDER BY percent DESC) AS T3 
                  WHERE T3.percent >1""")
    posts = c.fetchall()
  if POSTS[0] == "none":
    posts = ""
  db.close()
  return posts

"""function to populate the POSTS list with the question value"""
def add_post(content):
  POSTS.pop(0)
  POSTS.insert(0,content)

app = Flask(__name__)

# HTML template for the report page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Reporting Tool</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
    </style>
  </head>
  <body>
    <h1>Reporting Tool</h1>
    <form method=post>
      <div>
        <select name="content">
          <option value="none">Select Question</option>
          <option value="q1">What are the most popular three articles of all time?</option>
          <option value="q2">Who are the most popular article authors of all time?</option>
          <option value="q3">On which days did more than 1%% of requests lead to errors?</option>
        </select>
      </div>
      <br>
      <div><button id="go" type="submit">Answer</button></div>
    </form>
    <!-- post content will go here -->
%s
  </body>
</html>
'''


@app.route('/', methods=['GET'])
def main():
  '''Main page of the forum.'''
  if POSTS[0] == "none":
    POST = '''\
    <div class=post><p><em class=date>%s</em><br>%s</div>'''
    posts = ""
  if POSTS[0] == "q1":
    POST = '''\
    <div class=post>Number of article queries = %s<br>Title of article: %s</div>'''
    posts = "".join(POST % (name, bio) for bio, name in get_posts())
  if POSTS[0] == "q2":
    POST = '''\
    <div class=post>Article author: %s received %s views</div>'''
    posts = "".join(POST % (authorname,totalarticles) for authorname, totalarticles in get_posts())
  if POSTS[0] == "q3":
    POST = '''\
    <div class=post><br>On %s more than 1%% of the requests led to errors</div>'''
    posts = "".join(POST % (days) for days in get_posts())
  html = HTML_WRAP % posts
  return html


@app.route('/', methods=['POST'])
def post():
  '''New post submission.'''
  message = request.form['content']
  add_post(message)
  return redirect(url_for('main'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
