# ff_scrape
this thing scrapes the fantasy pros website for football player names, appends them to a new dictionary, then streams the fantasy football subreddit indefinitely and parses comments for matching player names. every hour, the script dumps the count into an sqlite3 database, which is created in the same directory as the code. i'm using the nltk module at the moment to identify proper names as an initial filter, but this is probably overkill and could be replaced with a simple re parser using the player dictionary.

to use, create a new app on reddit and get the client secret and client id info to pass into the Reddit() instance in the run_ff.py file.

requires praw, bs4, and nltk

# update (10/5/18)
added common player nicknames (e.g. obj for odell beckham jr., ajg for a.j. green, etc.) in the const.py file; added functionality for portioning out common first and last names (e.g. doling out a percentage of the name 'aaron' to aaron rodgers and aaron jones), combined the classes in the database_update.py file, added logging functionality to write nickname mentions and leftover proper nouns to file (located within 'log/' in the same folder as the code), scraping more player names from the fantasy pros website (includes scraping the ADP page and the fantasy football leaders pages), added a refresh option on scraping player names from fantasy pros site.
