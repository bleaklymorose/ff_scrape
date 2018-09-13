import praw

from player_class import FFStream


def main():

    stream = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='',
                         username='',
                         password='')

    FFStream(stream).run()


if __name__ == '__main__':
    main()
