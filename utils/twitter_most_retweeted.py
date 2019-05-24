import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_retweets_by_domain(domain: str, threshold: int = 10, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT query, tweet_link, tweet, retweet_count FROM twitter_most_retweeted
    WHERE query LIKE "%{}%" AND retweet_count > {} ORDER BY retweet_count DESC LIMIT 0,{};
    """.format(domain, threshold, limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows
