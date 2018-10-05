import urllib.request
import bs4 as bs
# from pprint import PrettyPrinter, pprint
from time import sleep
from const import URL_ADP, URL_LEAD


class ObtainPlayer:

    def __init__(self, pos):
        self.pos = pos
        self.uniques = set()
        self.names = set()
        self.intermediate = set()
        self.duplicate = set()
        self.player_dict = {}
        self.common_name_dict = {}

    def _uniques(self, player_name):

        self.names.add(player_name[0].lower())
        self.names.add(player_name[1].lower())

        # unique first -> last names
        if player_name[0].lower() in self.intermediate:
            self.duplicate.add(player_name[0].lower())
        else:
            self.intermediate.add(player_name[0].lower())

        if player_name[1].lower() in self.intermediate:
            self.duplicate.add(player_name[1].lower())
        else:
            self.intermediate.add(player_name[1].lower())

        self.uniques = self.names - self.duplicate

    @staticmethod
    def scrape_player(pos, url):

        back_off = 1
        for attempt in range(10):
            try:
                str_error = None
                sauce = urllib.request.urlopen(url + pos + '.php').read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                player = soup.find_all('a', {'class': 'player-name'})
            except urllib.request.HTTPError:
                print('...error opening fantasypros webpage')
                str_error = True
            if str_error:
                sleep(back_off)
                back_off *= 2
            elif attempt == 9:
                raise SystemExit('... unable to connect to fantasypros, terminating program')
            else:
                break

        return player

    def obtain_player_dict(self):

        for position in self.pos:
            # obtain an inclusive list of players from ADP and LEADERS pages
            print('...obtaining player list for pos: {}'.format(position))
            player = self.scrape_player(pos=position, url=URL_ADP)
            player.extend(i for i in self.scrape_player(pos=position, url=URL_LEAD) if i not in player)
            print('position: {0} number of players: {1}'.format(position, len(player)))

            # build a full player name dictionary
            for member in player:
                if member.string is not None:
                    name = member.string.split(' ')
                    self._uniques(name)
                    if len(name) == 2:
                        entry = dict(fullNameDB='', firstName='', lastName='', suffix='', pos='', pseudoName=[],
                                     count=0, sum=0, common_count=0, frac_count=0, tot_count=0, tot_sum=0)
                        fullName = name[0].lower() + name[1].lower()
                        entry["fullNameDB"] = ''.join(i for i in fullName if i.isalnum())
                        entry["firstName"] = name[0].lower()
                        entry["lastName"] = name[1].lower()
                        entry["pos"] = position
                        self.player_dict[name[0].lower() + ' ' + name[1].lower()] = entry
                    else:
                        entry = dict(fullNameDB='', firstName='', lastName='', suffix='', pos='', pseudoName=[],
                                     count=0, sum=0, common_count=0, frac_count=0, tot_count=0, tot_sum=0)
                        fullName = name[0].lower() + name[1].lower() + name[2].lower()
                        entry["fullNameDB"] = ''.join(i for i in fullName if i.isalnum())
                        entry["firstName"] = name[0].lower()
                        entry["lastName"] = name[1].lower()
                        entry["suffix"] = name[2].lower()
                        entry["pos"] = position
                        self.player_dict[name[0].lower() + ' ' + name[1].lower() + ' ' + name[2].lower()] = entry

    def obtain_common_player_dict(self):

        # build a common name dictionary
        for common_name in self.duplicate:
            entry = dict(fullNameDB='', count=0, sum=0, shared_players={})
            entry["fullNameDB"] = ''.join(i for i in common_name if i.isalnum())
            self.common_name_dict[common_name] = entry

        # populate the common name dictionary with shared entries
        for player in self.player_dict:
            first, last = self.player_dict[player]['firstName'], self.player_dict[player]['lastName']
            if first in self.common_name_dict:
                self.common_name_dict[first]['shared_players'][player] = 0
            if last in self.common_name_dict:
                self.common_name_dict[last]['shared_players'][player] = 0

