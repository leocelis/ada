# TODO: Add the last updated time
# TODO: add refresh time, should match the cron job
# TODO: add newsfeed section with games, streamers (new value, prev value, and delta)
# TODO: replace the powered by, with "ada-tool.com/twitch" url
# TODO: show games total viewers
# TODO: add countdown until next sync

import sys
import time

import emoji
from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import Screen

# colors
COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7

# style
A_BOLD = 1
A_NORMAL = 2
A_REVERSE = 3
A_UNDERLINE = 4

# Ada related
POWERED_BY_ADA = "powered by ada-tool.com"


def demo(screen):
    screen.clear()

    i = 0
    while True:
        # main interface
        date = time.strftime("%m/%d/%Y %H:%M:%S")
        screen.print_at(date,
                        int(screen.width / 2) - int(len(date) / 2),
                        1,
                        COLOUR_CYAN)
        screen.print_at(POWERED_BY_ADA,
                        int(screen.width / 2) - int(len(POWERED_BY_ADA) / 2),
                        screen.height - 1,
                        COLOUR_BLUE)

        # Top 10 games
        x = 25
        screen.print_at(u'{}TOP 10 STREAMS'.format(emoji.emojize(':trophy:')), x, 10, COLOUR_WHITE, A_BOLD)
        screen.print_at('-----------------------------------', x, 11, COLOUR_YELLOW)
        screen.print_at(u'1. Just Chatting {}'.format(emoji.emojize(':star:', use_aliases=True)), x, 12, COLOUR_WHITE)
        screen.print_at('2. Just Chatting', x, 13, COLOUR_WHITE)
        screen.print_at('3. Just Chatting', x, 14, COLOUR_WHITE)
        screen.print_at('4. Just Chatting', x, 15, COLOUR_WHITE)
        screen.print_at('5. Just Chatting', x, 16, COLOUR_WHITE)
        screen.print_at('6. Just Chatting', x, 17, COLOUR_WHITE)
        screen.print_at('7. Just Chatting', x, 18, COLOUR_WHITE)
        screen.print_at('8. Just Chatting', x, 19, COLOUR_WHITE)
        screen.print_at('9. Just Chatting', x, 20, COLOUR_WHITE)
        screen.print_at('10. Just Chatting', x, 21, COLOUR_WHITE)

        # Top 10 streams
        x = 80
        screen.print_at(u'{}TOP 10 GAMES'.format(emoji.emojize(':trophy:')), x, 10, COLOUR_WHITE, A_BOLD)
        screen.print_at('-----------------------------------', x, 11, COLOUR_YELLOW)
        screen.print_at(u'1. Just Chatting {}'.format(emoji.emojize(':star:', use_aliases=True)), x, 12, COLOUR_WHITE)
        screen.print_at('2. Just Chatting', x, 13, COLOUR_WHITE)
        screen.print_at('3. Just Chatting', x, 14, COLOUR_WHITE)
        screen.print_at('4. Just Chatting', x, 15, COLOUR_WHITE)
        screen.print_at('5. Just Chatting', x, 16, COLOUR_WHITE)
        screen.print_at('6. Just Chatting', x, 17, COLOUR_WHITE)
        screen.print_at('7. Just Chatting', x, 18, COLOUR_WHITE)
        screen.print_at('8. Just Chatting', x, 19, COLOUR_WHITE)
        screen.print_at('9. Just Chatting', x, 20, COLOUR_WHITE)
        screen.print_at('10. Just Chatting', x, 21, COLOUR_WHITE)

        # i += 1
        # screen.print_at(str(i), 10, 10, COLOUR_WHITE, A_BOLD)

        # press Q to quit
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return

        time.sleep(1)
        screen.refresh()


while True:
    try:
        Screen.wrapper(demo)
        sys.exit()
    except ResizeScreenError:
        pass
