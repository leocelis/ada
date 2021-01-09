from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

# Get Slack Bot Token from config.ini
slack_token = parser.get('slack', 'token')

# SCIM token
slack_scim_token = parser.get('slack', 'scim_token')
