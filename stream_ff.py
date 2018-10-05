from time import time, sleep

from prawcore.exceptions import PrawcoreException
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from logger import NicknameLog, FilteredLog
from fetch_player import ObtainPlayer
from database_update import AddToDB
from const import DATABASE, COMMON_DATABASE, POS, COMMON_NN, NN_LOG, FILTER_LOG


class FFStream:

    stop_words = set(stopwords.words("english"))

    def __init__(self, reddit, div=3600, refresh=False, write=False):

        # obtain praw object and instantiate ObtainPlayer object
        self.reddit = reddit
        self.player_object = ObtainPlayer(pos=POS)

        # obtain player dictionary and common player dictionary from player_object
        self.player_object.obtain_player_dict()
        self.player_object.obtain_common_player_dict()
        self.players = self.player_object.player_dict
        self.common_players = self.player_object.common_name_dict

        # write comments to file
        self.write = write

        # create time and time series division attributes
        self.day = time()
        self.time = time()
        self.div = div
        self.refresh_players = refresh

        # initiate a diagnostics object
        self.nn_log = NicknameLog(name='nickname', directory=NN_LOG)
        self.filter_log = FilteredLog(name='filtered', directory=FILTER_LOG)

    @staticmethod
    def rem_na(filtered_list):

        filtered_list = [i for i in filtered_list if i is not 'na']
        return filtered_list

    @classmethod
    def proper_noun_filter(cls, comments):

        proper_nouns = []
        word_list = [i for i in word_tokenize(comments) if i not in cls.stop_words]
        tokens = pos_tag(word_list)
        for i in tokens:
            if i[1] == 'NNP':
                proper_nouns.append(i[0].lower())

        print('Filtered words: {}'.format(tokens))
        print('Collected proper nouns: {}'.format(proper_nouns))
        return proper_nouns

    def write_comments_to_file(self, comment):

        try:
            if self.write:
                with open('corpus/comment_text.txt', 'a', encoding='utf-8') as file:
                    file.write(comment)
        except UnicodeEncodeError:
            print('emogee bullshit')

    def nick_name_count(self, mention):

        # catch common player nicknames
        for position in COMMON_NN:
            for player in COMMON_NN[position]:
                for nickname in COMMON_NN[position][player]:
                    nn_pack = nickname.split(' ')

                    # catch single word nicknames
                    if len(nn_pack) == 1:
                        for i in range(len(mention)):
                            if mention[i] == nn_pack[0]:
                                self.players[player]["count"] += 1
                                print('...nickname/player mentioned: {}/{}'.format(mention[i], player))
                                self.nn_log.log_nicknames(mention[i], player)
                                mention[i] = 'na'

                    # catch two word nicknames
                    elif len(nn_pack) == 2:
                        for i, j in zip(range(len(mention)), range(1, len(mention))):
                            potential_nn = mention[i] + ' ' + mention[j]
                            if potential_nn == nn_pack[0] + ' ' + nn_pack[1]:
                                self.players[player]["count"] += 1
                                print('...nickname/player mentioned: {}/{}'.format(potential_nn, player))
                                self.nn_log.log_nicknames(potential_nn, player)
                                mention[i], mention[j] = 'na', 'na'

                    # catch three word nicknames
                    elif len(nn_pack) == 3:
                        for i, j, k in zip(range(len(mention)), range(1, len(mention)), range(2, len(mention))):
                            potential_nn = mention[i] + ' ' + mention[j] + ' ' + mention[k]
                            if potential_nn == nn_pack[0] + ' ' + nn_pack[1] + ' ' + nn_pack[2]:
                                self.players[player]["count"] += 1
                                print('...nickname/player mentioned: {}/{}'.format(potential_nn, player))
                                self.nn_log.log_nicknames(potential_nn, player)
                                mention[i], mention[j], mention[k] = 'na', 'na', 'na'
                    # go to next
                    else:
                        continue

        mention = self.rem_na(mention)
        print('filtered nickname list: {}'.format(mention))
        return mention

    def full_count(self, mention):

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

        mention = self.rem_na(mention)
        print('filtered list: {}'.format(mention))
        return mention

    def unique_count(self, mention):

        # catch unique names
        for i in range(len(mention)):
            if mention[i] in self.player_object.uniques:
                for player in self.players:
                    if self.players[player]['firstName'] == mention[i]:
                        self.players[player]['count'] += 1
                        print('...player mentioned: {}'.format(mention[i]))
                        mention[i] = 'na'
                    elif self.players[player]['lastName'] == mention[i]:
                        self.players[player]['count'] += 1
                        print('...player mentioned: {}'.format(mention[i]))
                        mention[i] = 'na'

        mention = self.rem_na(mention)
        print('filtered unique list: {}'.format(mention))
        return mention

    def common_count(self, mention):

        # catch common player names
        for i in range(len(mention)):
            if mention[i] in self.player_object.duplicate:
                self.common_players[mention[i]]["count"] += 1
                print('...common player name mentioned: {}'.format(mention[i]))
                mention[i] = 'na'

        mention = self.rem_na(mention)
        print('filtered final list: {}'.format(mention))
        return mention

    def sort_common(self):

        # dump counts of common player names into the shared players key in the common_players dictionary
        for entry in self.players:
            first, last = self.players[entry]["firstName"], self.players[entry]["lastName"]
            if first in self.common_players:
                self.common_players[first]["shared_players"][entry] = self.players[entry]["count"]
            if last in self.common_players:
                self.common_players[last]["shared_players"][entry] = self.players[entry]["count"]

        # add common counts to players with shared names, using a fractional scheme
        sorted_common = sorted(self.common_players.items(), key=lambda key: key[1]["count"])
        for common in sorted_common:
            count = 0
            for player in common[1]['shared_players']:
                count += common[1]['shared_players'][player]
            for player in common[1]['shared_players']:
                if count != 0:
                    count_share = int(round(common[1]["count"] * (common[1]['shared_players'][player] / count)))
                    self.players[player]["common_count"] += common[1]["count"]
                    self.players[player]["frac_count"] += count_share
                    self.players[player]["tot_count"] = self.players[player]["frac_count"] + self.players[player]["count"]

    def update_metrics(self):

        for entry in self.players:
            self.players[entry]["sum"] += self.players[entry]["count"]
            self.players[entry]["tot_sum"] += self.players[entry]["tot_count"]

        for common_entry in self.common_players:
            self.common_players[common_entry]["sum"] += self.common_players[common_entry]["count"]

    def write_to_db(self):

        print('\n**writing to player database**')
        with AddToDB(DATABASE, self.players) as database:
            database.add_tables()
            database.data_entry()
            print(database.poopy_butt_rodgers())

        print('**writing to common player database**')
        with AddToDB(COMMON_DATABASE, self.common_players) as common_database:
            common_database.add_tables_common()
            common_database.data_entry_common()

    def reset_counts(self):

        for entry in self.players:
            self.players[entry]["count"] = 0
            self.players[entry]["common_count"] = 0
            self.players[entry]["frac_count"] = 0
            self.players[entry]["tot_count"] = 0

        for common_entry in self.common_players:
            self.common_players[common_entry]["count"] = 0
            for shared_player in self.common_players[common_entry]["shared_players"]:
                self.common_players[common_entry]["shared_players"][shared_player] = 0

    def run(self):

        self.write_to_db()
        running = True

        while running:
            try:
                for comment in self.reddit.subreddit('fantasyfootball').stream.comments(pause_after=0):
                    # remove exponential backoff from praw.models.util.stream_generator()
                    if comment is None:
                        print(20 * '-')
                        print('**no comments found for this request**')
                        if time() - self.time > self.div:
                            print(self.player_object.player_dict)
                            self.sort_common()
                            self.update_metrics()
                            self.write_to_db()
                            self.reset_counts()
                            # reset time
                            self.time = time()
                        continue

                    print(20 * '-')
                    print(comment.body)
                    print(comment.parent_id)
                    proper_nouns = self.proper_noun_filter(comment.body)
                    # write comments to a file to serve as a corpus
                    self.write_comments_to_file(comment.body)
                    # filter player mentions
                    final_mentions = self.common_count(self.unique_count(self.full_count(self.nick_name_count(proper_nouns))))
                    if len(final_mentions) > 0:
                        self.filter_log.log_final_filtered_list(final_mentions)
                    # dump metrics to sqlite database
                    if time() - self.time > self.div:
                        print(self.player_object.player_dict)
                        self.sort_common()
                        self.update_metrics()
                        self.write_to_db()
                        self.reset_counts()
                        # reset time
                        self.time = time()

                    # refresh player dictionary
                    if self.refresh_players and time() - self.day > self.refresh_players:
                        self.player_object = ObtainPlayer(pos=POS)
                        self.player_object.obtain_player_dict()
                        self.player_object.obtain_common_player_dict()
                        self.players = self.player_object.player_dict
                        self.common_players = self.player_object.common_name_dict
                        self.day = time()

            except PrawcoreException as e:
                print('...error connecting to server {}'.format(e))
                print('...attempting to reestablish connection')
                sleep(60)
