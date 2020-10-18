# TODO: archive old data to s3

import os
import sys

from twitchAPI.twitch import Twitch

sys.path.append(os.path.dirname(os.getcwd()))
from ada.twitch.utils import get_top_game_last_entry, insert_top_game_stats, get_top_stream_last_entry, \
    insert_top_stream_stats

# settings
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
MAX_PAGES = 5  # times 100

# create instance of twitch API
twitch = Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
twitch.authenticate_app([])

# ====================
# get top streamers
# ====================
cursor = 1
page = 1
while cursor:
    if cursor == 1:
        streams = twitch.get_streams(first=100)
    else:
        streams = twitch.get_streams(after=cursor, first=100)

    for stream in streams.get('data', {}):
        print(stream)
        stream_id = stream.get('id')

        if stream_id:
            r = get_top_stream_last_entry(stream_id=stream_id)

            # get the last viewer count
            if r:
                last_viewer_count = r.get('viewer_count', 0)
            else:
                last_viewer_count = stream.get('viewer_count', 0)

            insert_top_stream_stats(stream, last_viewer_count)

    cursor = streams.get('pagination', {}).get('cursor', None)
    page += 1

    if page == MAX_PAGES:
        break

# ====================
# get top games
# ====================
current_position = 0
cursor = 1
page = 1
while cursor:
    if cursor == 1:
        games = twitch.get_top_games(first=100)
    else:
        games = twitch.get_top_games(after=cursor, first=100)

    for game in games.get('data', {}):
        print(game)
        game_id = game.get('id')

        if game_id:
            r = get_top_game_last_entry(game_id=game_id)

            # increment the position
            current_position += 1

            # get the last position
            if r:
                last_position = r.get('current_position', 0)
            else:
                # the first time the last position is the current one
                last_position = current_position

            insert_top_game_stats(game, current_position, last_position)

    cursor = games.get('pagination', {}).get('cursor', None)
    page += 1

    if page == MAX_PAGES:
        break
