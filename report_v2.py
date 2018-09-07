#!/usr/bin/env python3
# A reporting tool to answer some questions

import psycopg2
import bleach
import datetime

DBNAME = "news"


def get_posts():

    # Connect to the database, execute each query, and write the output to file
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT articles.title, count(*) AS num
                   FROM articles
                   JOIN log
                     ON log.path LIKE '%'||articles.slug||'%'
               GROUP BY articles.title
               ORDER BY num DESC
                  LIMIT 3""")
    posts = c.fetchall()
    f = open("report_result.txt", "a")
    f.write('1. What are the most popular three articles of all time?:\r\n')
    f.write('\r\nThe most popular article is \'' +
            str(posts[0][0]) + '\' with ' + str(posts[0][1]) + ' views\r\n')
    f.write('The 2nd most popular article is \'' +
            str(posts[1][0]) + '\' with ' + str(posts[1][1]) + ' views\r\n')
    f.write('The 3rd most popular article is \'' +
            str(posts[2][0]) + '\' with ' + str(posts[2][1]) + ' views\r\n')
    f.close
    del posts[:]
    c.execute(""" SELECT DISTINCT totalcount.authorname,
                                  sum(totalcount.articlecount) AS totalarticles
                             FROM (
                                   SELECT count(log.time) AS articlecount,
                                          authors.name AS authorname
                                     FROM articles
                                     JOIN log
                                       ON log.path LIKE '%'||articles.slug||'%'
                                     JOIN authors
                                       ON authors.id = articles.author
                                 GROUP BY articles.slug, articles.author,
                                          authors.name) AS totalcount
                         GROUP BY totalcount.authorname
                         ORDER BY totalarticles DESC""")
    posts = c.fetchall()
    f = open("report_result.txt", "a")
    f.write('\r\n2. Who are the most popular'
            ' article authors of all time?:\r\n')
    i = 0
    f.write('\r\n')
    while i < int(len(posts)):
        f.write(str(i+1) + '. ' + str(posts[i][0]) + ' - ' +
                str(posts[i][1]) + ' views\r\n')
        i += 1
    f.close
    del posts[:]
    c.execute("""SELECT T3.days
                   FROM (
                         SELECT T1.days AS days,
                                ROUND(100*T1.badreqs/T2.totalreqs,2) AS percent
                   FROM (
                         SELECT distinctdays.days AS days,
                                count(log.time) AS badreqs
                   FROM log
                   JOIN (
                         SELECT DISTINCT date(log.time) AS days
                                    FROM log) AS distinctdays
                     ON date(log.time) = distinctdays.days
                  WHERE log.status LIKE '%404%'
               GROUP BY distinctdays.days) AS T1
                   JOIN (
                        SELECT distinctdays.days AS days,
                               count(log.time) AS totalreqs
                   FROM log
                   JOIN (
                        SELECT DISTINCT date(log.time) AS days
                                   FROM log) AS distinctdays
                                     ON date(log.time) = distinctdays.days
                               GROUP BY distinctdays.days) AS T2
                                     ON T1.days = T2.days
                               ORDER BY percent DESC) AS T3
                  WHERE T3.percent > 1""")
    posts = c.fetchall()
    f = open("report_result.txt", "a")
    f.write('\r\n3. On which days did more than'
            '1% of requests lead to errors?:\r\n')
    f.write('\r\n')
    i = 0
    while i < int(len(posts)):
        f.write(str(i + 1) + '. On ' + str(posts[i][0]) +
                ' more than 1% of requests returned errors\r\n')
        i += 1
    f.close
    del posts[:]


get_posts()
