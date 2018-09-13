import urllib.request
import bs4 as bs
from time import sleep


def obtain_player_dict():

    pos_list = ['qb', 'rb', 'wr', 'te', 'k']
    player_dict = {}

    for position in pos_list:

        # try connecting to fantasy pros site and scraping player data
        back_off = 1
        for attempt in range(10):
            print('...obtaining player list for pos: {}'.format(position))
            try:
                str_error = None
                sauce = urllib.request.urlopen('https://www.fantasypros.com/nfl/adp/' + position + '.php').read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                player = soup.find_all('a', {'class': 'player-name'})
                print('position: {0} number of players: {1}'.format(position, len(player)))
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

        for member in player:
            if member.string is not None:
                # player_list.append(member.string)
                name = member.string.split(' ')
                if len(name) == 2:
                    entry = dict(fullNameDB='', firstName='', lastName='', suffix='', pos='', pseudoName=[], count=0)
                    fullName = name[0].lower() + name[1].lower()
                    entry["fullNameDB"] = ''.join(i for i in fullName if i.isalnum())
                    entry["firstName"] = name[0].lower()
                    entry["lastName"] = name[1].lower()
                    entry["pos"] = position
                    # player_dict[name[0].lower()] = entry
                    player_dict[name[0].lower() + ' ' + name[1].lower()] = entry
                else:
                    entry = dict(fullNameDB='', firstName='', lastName='', suffix='', pos='', pseudoName=[], count=0)
                    fullName = name[0].lower() + name[1].lower() + name[2].lower()
                    entry["fullNameDB"] = ''.join(i for i in fullName if i.isalnum())
                    entry["firstName"] = name[0].lower()
                    entry["lastName"] = name[1].lower()
                    entry["suffix"] = name[2].lower()
                    entry["pos"] = position
                    # player_dict[name[0].lower()] = entry
                    player_dict[name[0].lower() + ' ' + name[1].lower() + ' ' + name[2].lower()] = entry

    return player_dict
