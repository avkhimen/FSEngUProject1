# Description #

_newsdata.sql_ file contains the _news_ database. The _news_ sql database contains the three tables: 
articles, authors, and log. `report_v2.py` file is a reporting tool that when ran allows one to answer 
the following 3 questions based on the _news_ sql database:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Installation and Usage ##

### Installation ###

In order to run the `report_v2.py` file you must have access to a Linux virtual machine. Access the 
Linux VM by installing `vagrant`. After installing `vagrant` run it in the terminal of your
choice.

### Usage ###

Download the `report_v2.py` and the _newsdata.sql_ files. Then place them into the `/vagrant` directory. 
In order to use the `report_v2.py` tool open up `vagrant`, open up your terminal and navigate to the 
directory where the `report.py_v2` and _newsdata.sql_ files are located. While vagrant is up, run the 
`python report_v2.py` command in your terminal. 

Now navigate to the folder where your `report_v2.py` file is stored. In that directory you will have
a new file called `report_result.txt`. Open the file to see the results of the report.

## Design of the Code ##

The name of the database is stored in the `DBNNAME` variable. `get_posts()` function connects to the 
_news_ database, then for every SQL query, it opens the `report_result.txt` file, and finally writes 
the query output to the file. Running the `get_posts()` function creates the report.   
