#Description#

_newsdata.sql_ file contains the _news_ database. The _news_ sql database contains the three tables: 
articles, authors, and log. `report.py` file is a reporting tool that when ran allows one to answer 
the following 3 questions based on the _news_ sql database:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

##Installation and Usage##

###Installation###

In order to run the `report.py` file you must have access to a Linux virtual machine. Access the 
Linux VM by installing `vagrant`. After installing `vagrant` run it in the terminal of your
choice.

###Usage###

Download the `report.py` and the _newsdata.sql_ files. Then place them into the `/vagrant` directory. 
In order to use the `report.py` tool open up `vagrant`, open up your terminal and navigate to the 
directory where the `report.py` and _newsdata.sql_ files are located. While vagrant is up, run the 
`python report.py` command in your terminal. 

Now open up the internet browser of your choice and navigate to `https://localhost:8000`. The report
will be displayed. At this point you will be able to select the question you want answered and by 
clicking the "Answer" button the report results will be displayed. 

##Design of the Code##

The framework for building the `report.py` file is `Flask`. The name of the database is stored in the
`DBNNAME` variable. `get_posts` function connects to the _news_ database and defines the `psql` 
queries that will be executed based on the value in the `POSTS` list once the file is ran in the 
localhost. `add_post` function takes the value of the questions being asked from the dropdown list
and stores it in the `POSTS` list. `HTML_WRAP` defines the html layout of the report.



