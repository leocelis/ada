import logging.config

import yaml

# Facebook Ads Optimization
DATA_FOLDER = "./data"

# Content Discovery
SHARETHIS_THRESHOLD = 2  # min total actions in Share This
FACEBOOK_SHARES_THRESHOLD = 2  # min shares a link should have
TWITTER_RETWEETS_THRESHOLD = 5  # min retweets a tweet should have
TWITTER_WAIT_REQUESTS = 2  # wait seconds between requests
TWITTER_HISTORY_COUNT = 400  # how many tweets in the past we will consider
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
