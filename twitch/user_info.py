import os
import ujson

from pygments import highlight, lexers, formatters
from twitchAPI.twitch import Twitch

# settings
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')

# create instance of twitch API
twitch = Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
twitch.authenticate_app([])

# get ID of user
user_info = twitch.get_users(logins=['inthevalley2020'])
formatted_json = ujson.dumps(user_info, sort_keys=True, indent=4)
colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
print(colorful_json)
