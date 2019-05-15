import os
import sys
from time import sleep

from twython import Twython

# add parent dir
sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import TWITTER_WAIT_REQUESTS, TWITTER_HISTORY_COUNT, TWITTER_RETWEETS_THRESHOLD

# twitter vars
TWITTER_APP_KEY = os.environ.get('TWITTER_APP_KEY')
TWITTER_APP_SECRET = os.environ.get('TWITTER_APP_SECRET')

# create twitter connection
twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth = twitter.get_authentication_tokens()


def search_tweets(query: str, retweets: bool = False, result_type: str = 'mixed') -> list:
    """
    Search tweets. Only return tweets with retweets >= threshold

    :param query:
    :param retweets:
    :param result_type: mixed, recent, popular
    :return: a list of tweets
    """
    tweets_count = 0
    next_max_id = 0
    tweets = list()

    # include retweets?
    if not retweets:
        query = "{} -filter:retweets".format(query)  # no retweets

    print("\nRetrieving tweets for: {}".format(query))

    while tweets_count <= TWITTER_HISTORY_COUNT:
        try:
            # get first 100
            if tweets_count == 0:
                results = twitter.search(q=query, result_type=result_type, include_entities="false", lang="en",
                                         count='100')
            else:
                # search next page
                results = twitter.search(q=query, result_type=result_type, include_entities="false", lang="en",
                                         max_id=next_max_id)
            sleep(TWITTER_WAIT_REQUESTS)
        except Exception as e:
            print("\nERROR: {}".format(str(e)))
            continue

        # keep tweets in mem
        for r in results['statuses']:
            tweets_count += 1
            retweets = r.get('retweet_count', 0)
            tweet_id = r['id_str']
            user_name = r['user']['screen_name']
            tweet_link = "https://twitter.com/{}/status/{}".format(user_name, tweet_id)

            if retweets >= TWITTER_RETWEETS_THRESHOLD:
                print("\n{} - {} - Retweets {}...".format(r['text'], tweet_link, retweets))
                tweets.append(r)

        # get next page
        try:
            next_results_url_params = results['search_metadata']['next_results']
            next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]
        except:
            break

    return tweets
