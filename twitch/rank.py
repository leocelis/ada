# TODO: Add the last updated time
# TODO: add refresh time, should match the cron job
# TODO: add newsfeed section with games, streamers (new value, prev value, and delta)
# TODO: replace the powered by, with "ada-tool.com/?industry" url
# TODO: show games total viewers
# TODO: add countdown until next sync for 10 sec
# TODO: pull the data directly from Twitch
# TODO: remove the ada tool until have advanced analytics
# TODO: Put the timezone in the hour
# TODO: fatest jumper: relation between start at and delta increase

import os
import sys
import time

import emoji
from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import Screen
from twitchAPI.twitch import Twitch

sys.path.append(os.path.dirname(os.getcwd()))
from ada.twitch.utils import get_top_game, get_top_streamer

# SETTINGS
COUNTDOWN = 10  # seconds
COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7
A_BOLD = 1
A_NORMAL = 2
A_REVERSE = 3
A_UNDERLINE = 4

# TWITCH
MAX_RESULTS = 10
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
twitch = Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
twitch.authenticate_app([])

# RANK
POWERED_BY_ADA = "more stats in www.ada-tool.com/twitch"
TOP_GAMES_TITLE = u'{} TOP {} GAMES LIVE'
TOP_STREAMS_TITLE = u'{} TOP {} STREAMERS LIVE'
TOP_STREAMER_RECORD = "STREAMER CONCURRENT-VIEWERS WORLD-RECORD: {} ({:,})"
TOP_GAME_RECORD = "GAME TOP 1 MOST-TIMES WORLD-RECORD: {}"


def decide_emoji(pos):
    e = ""
    if pos == 1:
        e = emoji.emojize(':star:', use_aliases=True)
    return e


def get_top_games():
    global twitch
    games = twitch.get_top_games(first=MAX_RESULTS)
    return games.get('data', {})


def print_games(games, screen, x, y):
    pos = 1

    for game in games:
        screen.print_at(u'{}. {} {}'.format(pos, game.get("name", "N/A"), decide_emoji(pos)),
                        x,
                        y,
                        COLOUR_WHITE)
        pos += 1
        y += 1


def get_top_streams():
    global twitch
    streams = twitch.get_streams(first=MAX_RESULTS)
    return streams.get('data', {})


def print_streams(streams, screen, x, y):
    pos = 1
    for stream in streams:
        t = "{} ({:,})".format(stream.get("user_name", "N/A"),
                               stream.get("viewer_count", 0))
        screen.print_at(u'{}. {} {}'.format(pos, t, decide_emoji(pos)),
                        x,
                        y,
                        COLOUR_WHITE)
        pos += 1
        y += 1


def rank(screen):
    # countdown
    global COUNTDOWN
    counting = COUNTDOWN

    screen.clear()

    # # ada message
    # screen.print_at(POWERED_BY_ADA,
    #                 int(screen.width / 2) - int(len(POWERED_BY_ADA) / 2),
    #                 screen.height - 1,
    #                 COLOUR_BLUE)

    i = 0
    while True:
        # twitch data
        if counting == COUNTDOWN:
            # get data
            games = get_top_games()
            streams = get_top_streams()
            top_game = get_top_game()
            top_streamer, viewers = get_top_streamer()

            # clean screen
            screen.clear()

            # records
            title = TOP_GAME_RECORD.format(top_game)
            screen.print_at(title,
                            10,
                            7,
                            COLOUR_CYAN)

            title = TOP_STREAMER_RECORD.format(top_streamer, viewers)
            screen.print_at(title,
                            10,
                            9,
                            COLOUR_CYAN)

        # countdown
        if counting == 0:
            counting = COUNTDOWN
        else:
            counting -= 1

        # countdown
        refresh = "Refresh in {} ".format(counting)
        screen.print_at(refresh,
                        1,
                        1,
                        COLOUR_CYAN)

        # hour
        date = time.strftime("%m/%d/%Y %H:%M:%S")
        screen.print_at(date,
                        # int(screen.width / 2) - int(len(date) / 2),
                        int(screen.width) - (len(date) + 1),
                        1,
                        COLOUR_CYAN)

        # Top games
        x = 10
        y = 13
        screen.print_at(TOP_GAMES_TITLE.format(emoji.emojize(':trophy:'), MAX_RESULTS), x, y, COLOUR_WHITE, A_BOLD)
        screen.print_at('-----------------------------------', x, y + 1, COLOUR_YELLOW)
        print_games(games, screen, x, y + 2)

        # Top streams
        x = 64
        y = 13
        screen.print_at(TOP_STREAMS_TITLE.format(emoji.emojize(':trophy:'), MAX_RESULTS), x, y, COLOUR_WHITE, A_BOLD)
        screen.print_at('-----------------------------------', x, y + 1, COLOUR_YELLOW)
        print_streams(streams, screen, x, y + 2)

        # i += 1
        # screen.print_at(str(i), 10, 10, COLOUR_WHITE, A_BOLD)

        # press Q to quit
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return

        time.sleep(1)
        screen.refresh()
        # screen.reset()


while True:
    try:
        Screen.wrapper(rank)
        sys.exit()
    except ResizeScreenError:
        pass
