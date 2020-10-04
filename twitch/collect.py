import os
from time import sleep
from twitchAPI.twitch import Twitch

TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')

# create instance of twitch API
twitch = Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
twitch.authenticate_app([])

# get ID of user
user_info = twitch.get_users(logins=['inthevalley2020'])
# print(user_info)
user_id = user_info['data'][0]['id']

# get top games
# games = twitch.get_top_games()
# formatted_json = ujson.dumps(games, sort_keys=True, indent=4)
# colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
# print(colorful_json)

# paginate games results
cursor = 1
while cursor:
    if cursor == 1:
        games = twitch.get_top_games()
    else:
        games = twitch.get_top_games(after=cursor)

    for game in games.get('data', {}):
        print(game.get('name', ""))

    cursor = games.get('pagination', {}).get('cursor', "")
    sleep(1)
