"""
Twitter Search Tweets API reference:
https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
"""
import os
import sys
from time import sleep

import ujson
from twython import Twython

# add parent dir
sys.path.append(os.path.dirname(os.getcwd()))
from ada.config import TWITTER_RETWEETS_THRESHOLD, TWITTER_WAIT_REQUESTS, TWITTER_HISTORY_COUNT, TWITTER_KEYWORDS
from ada.utils.conn import get_mysql_conn

# mysql vars
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# twitter vars
TWITTER_APP_KEY = os.environ.get('TWITTER_APP_KEY')
TWITTER_APP_SECRET = os.environ.get('TWITTER_APP_SECRET')

# create twitter connection
twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth = twitter.get_authentication_tokens()


def sync_tweets(keyword: str) -> None:
    query = "{} -filter:retweets".format(keyword)  # no retweets
    tweets_count = 0
    next_max_id = 0

    print("\nRetrieving tweets for keyword: {}".format(keyword))

    while tweets_count <= TWITTER_HISTORY_COUNT:
        # mixed = popular & recent
        try:
            # get first 100
            if tweets_count == 0:
                results = twitter.search(q=query, result_type="mixed", include_entities="false", lang="en",
                                         count='100')
            else:
                # search next page
                results = twitter.search(q=query, result_type="mixed", include_entities="false", lang="en",
                                         max_id=next_max_id)
        except Exception as e:
            print("\nERROR: {}".format(str(e)))
            continue

        # keep tweets in mem
        for result in results['statuses']:
            tweets_count += 1
            retweets = result.get('retweet_count', 0)
            # print("\n{} - *** Retweets {}...".format(result['text'], retweets))
            print("Retweets {}...".format(retweets))

            # save it if retweets is greater than threshold
            if retweets >= TWITTER_RETWEETS_THRESHOLD:
                save_tweet(t=result, keyword=keyword)

        # get next page
        try:
            next_results_url_params = results['search_metadata']['next_results']
            # print("\nNext results: {}".format(next_results_url_params))
            next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]
        except:
            print("\nNO MORE RESULTS!")
            break

        print("\nTweets count: {}".format(tweets_count))
        sleep(TWITTER_WAIT_REQUESTS)

    return


def save_tweet(t: dict, keyword: str) -> None:
    conn = get_mysql_conn()

    cursor = conn.cursor()

    retweet_count = int(t.get('retweet_count', 0))
    created_at = t['created_at']
    tweet_id = t['id_str']
    tweet = t['text']
    user_id = t['user']['id_str']
    user_name = t['user']['screen_name']
    blob = ujson.dumps(t)
    tweet_link = "https://twitter.com/{}/status/{}".format(user_name, tweet_id)
    # TODO: add a site_link field and extract the link from the tweet

    sql = """
    INSERT INTO twitter_most_retweeted(created_at, tweet_id, retweet_count, tweet, user_id, user_name,
    tweet_blob, tweet_link, keyword)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("\nSaving tweet: {}...".format(tweet_link))

    try:
        cursor.execute(sql, (created_at, tweet_id, retweet_count, tweet, user_id, user_name, blob, tweet_link, keyword))
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return


# search by keyword
for k in TWITTER_KEYWORDS:
    sync_tweets(keyword=k)
