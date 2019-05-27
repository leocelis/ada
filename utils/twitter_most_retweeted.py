import os
import sys

import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_retweets_by_domain(domain: str, threshold: int = 10, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM twitter_most_retweeted
    WHERE query LIKE "%{}%" AND retweet_count > {} ORDER BY retweet_count DESC LIMIT 0,{};
    """.format(domain, threshold, limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def check_retweet_exists(tweet_id: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT tweet_id FROM twitter_most_retweeted WHERE tweet_id = "{}"
    """.format(tweet_id)

    try:
        r = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()

    if r > 0:
        return True

    return False


def save_link_retweets(query: str, t: dict) -> None:
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

    sql = """
    INSERT INTO twitter_most_retweeted(created_at, tweet_id, retweet_count, tweet, user_id, user_name,
    tweet_blob, tweet_link, query)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("\nSaving tweet: {}...".format(tweet_link))

    try:
        cursor.execute(sql, (created_at, tweet_id, retweet_count, tweet, user_id, user_name, blob, tweet_link, query))
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_link_retweets(query: str, t: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    retweet_count = int(t.get('retweet_count', 0))
    tweet_id = t['id_str']
    user_name = t['user']['screen_name']
    blob = ujson.dumps(t)
    tweet_link = "https://twitter.com/{}/status/{}".format(user_name, tweet_id)

    sql = """
    UPDATE twitter_most_retweeted
    SET retweet_count = {},
    tweet_blob = '{}'
    WHERE tweet_id = '{}'
    """.format(retweet_count, blob, tweet_id)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return
