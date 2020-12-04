import logging.config

import yaml

# allowed URLS
ALLOWED_URLS = ["http://localhost:3000", "https://dashboard.leocelis.com", "https://ada.leocelis.com",
                "https://www.leocelis.com", "https://leocelis.com", "https://api.ada-tool.com",
                "https://www.ada-tool.com"]

# ignore the platforms domains
IGNORE_DOMAINS = ['facebook.com', 'linkedin.com', 'twitter.com', 'twitch.com',
                  'whatsapp.com', 'google.com', 'printfriendly.com', 'bufferapp.com', 'outlook.com',
                  'gmail.com']

# Facebook Ads Optimization
DATA_FOLDER = "./data"

# Content Discovery
SUMMARY_THRESHOLD = 5  # min total shares to make it in the summary table
SHARETHIS_THRESHOLD = 5  # min total actions in Share This
FACEBOOK_SHARES_THRESHOLD = 5  # min shares a link should have
TWITTER_RETWEETS_THRESHOLD = 5  # min retweets a tweet should have
TWITTER_WAIT_REQUESTS = 2  # wait seconds between requests
TWITTER_HISTORY_COUNT = 200  # how many tweets in the past we will consider
TWITTER_KEYWORDS = ['martech',
                    '"ad tech"',
                    'adtech',
                    '"performance marketing"',
                    '"growth marketing"',
                    '"martech stack"',
                    '"conversion metrics"',
                    # '"affiliating marketing"',
                    '"customer acquisition cost"',
                    '"customer cost of acquisition"',
                    # '"viral loop"',
                    '"life cycle marketing"',
                    '"predict growth"',
                    '"mobile attribution partners"',
                    '"lifecycle marketing"',
                    '"mobile stack"',
                    '"attribution partners"',
                    '"mobile growth stack"',
                    '"modeling growth"',
                    '"mar tech"',
                    '"stack market"',
                    '"chief martech"',
                    '"marketing technology landscape"',
                    '"marketing landscape"',
                    '"martech stack"',
                    '"marketing stack"',
                    '"hacking marketing"',
                    '"chief marketing technology"'
                    '"ad tech conference"',
                    '"adtech conference"',
                    '"ad tech company"',
                    '"adtech company"',
                    '"marketing technology conference"',
                    '"marketing tech conferences"',
                    '"marketing automation conference"',
                    '"analytics for marketers"',
                    # 'socialcode',
                    '"data analytics for marketers"',
                    '"data analytics marketing"',
                    '"customers engagement"',
                    '"growth hacking"']
# logging
log_yaml_file = 'logger.yaml'

with open(log_yaml_file, 'r') as f:
    log_config_dict = yaml.safe_load(f)
    f.close()

logging.config.dictConfig(log_config_dict)
log = logging.getLogger(__name__)
