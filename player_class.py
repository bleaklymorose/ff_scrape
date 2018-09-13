from time import time, sleep

from prawcore.exceptions import PrawcoreException
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from util import obtain_player_dict
from database_class import DataBase, AddToDB
from const import DATABASE


class FFStream:

    stop_words = set(stopwords.words("english"))

    def __init__(self, reddit, write=True):

        self.reddit = reddit
        self.players = obtain_player_dict()
        self.write = True
        self.time = time()

    def write_comments_to_file(self, comment):

        try:
            if self.write:
                with open('corpus/comment_text.txt', 'a', encoding='utf-8') as file:
                    file.write(comment)
        except UnicodeEncodeError:
            print('emogee bullshit')

    def count(self, mention):

        # catch full name of player
        for i, j in zip(range(len(mention)), range(1, len(mention))):
            full_name = mention[i] + ' ' + mention[j]
            if full_name in self.players.keys():
                print('...player mentioned: {}'.format(full_name))
                self.players[full_name]['count'] += 1
                mention[i], mention[j] = 'na', 'na'

        # catch players with a suffix
        for i, j, k in zip(range(len(mention)), range(1, len(mention)), range(2, len(mention))):
            full_name = mention[i] + ' ' + mention[j] + ' ' + mention[k]
            if full_name in self.players.keys():
                print('...player mentioned: {}'.format(full_name))
                self.players[full_name]['count'] += 1
                mention[i], mention[j], mention[k] = 'na', 'na', 'na'
        print('filtered list: {}'.format(mention))

    @classmethod
    def proper_noun_filter(cls, comments):

        player_mention = []
        word_list = [i for i in word_tokenize(comments) if i not in cls.stop_words]
        tokens = pos_tag(word_list)
        for i in tokens:
            if i[1] == 'NNP':
                player_mention.append(i[0].lower())
        print('Filtered words: {}'.format(tokens))
        print('Collected proper nouns: {}'.format(player_mention))
        return player_mention

    def write_to_db(self):

        print('*writing to database')
        with DataBase(DATABASE) as cursor:
            database = AddToDB(cursor, self.players)
            database.add_tables()
            database.data_entry()
            print(database.poopy_butt_rodgers())

    def reset_count(self):

        for entry in self.players:
            self.players[entry]["count"] = 0

    def run(self):

        self.write_to_db()
        running = True
        while running:
            try:
                for comment in self.reddit.subreddit('fantasyfootball').stream.comments():

                    print(20 * '-')
                    print(comment.body)
                    print(comment.parent_id)
                    player_mention = self.proper_noun_filter(comment.body)
                    # self.write_comments_to_file(comment.body)
                    self.count(player_mention)
                    if time() - self.time > 3600:
                        self.write_to_db()
                        self.reset_count()
                        self.time = time()

            except PrawcoreException as e:
                print('...error connecting to server {}'.format(e))
                print('...attempting to reestablish connection')
                sleep(60)
