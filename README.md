# ff_scrape
this thing scrapes the fantasy pros website for football player names, appends them to a new dictionary, then streams the fantasy football subreddit indefinitely and parses comments for matching player names. every hour, the script dumps the count into an sqlite3 database, which is created in the same directory as the code. i'm using the nltk module at the moment to identify proper names as an initial filter, but this is probably overkill and could be replaced with a simple re parser using the player dictionary.

to use, create a new app on reddit and get the client secret and client id info to pass into the Reddit() instance in the run_ff.py file.

requires praw, bs4, and nltk
