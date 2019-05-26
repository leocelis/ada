import os
import sys

import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_domains():
    """
    Get all domains

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM domain_stats;
    """

    cursor.execute(sql)
    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def update_domain_fb_shares(domain: str, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    fb_shares = r.get('engagement', {}).get('share_count', 0)
    fb_graph_object = ujson.dumps(r)

    sql = """
    UPDATE domain_stats
    SET facebook_shares = {},
    fb_object = '{}'
    WHERE domain = '{}'
    """.format(fb_shares, fb_graph_object, domain)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_domain_sharethis_total(domain: str, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    total = int(r.get('total', 0))
    blob = ujson.dumps(r)

    sql = """
    UPDATE domain_stats
    SET sharethis_total = {},
    sharethis_object = '{}'
    WHERE domain = '{}'
    """.format(total, blob, domain)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_domain_retweets(domain: str, tweets: int, retweets: int, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    blob = ujson.dumps(r)

    sql = """
    UPDATE domain_stats
    SET twitter_retweets = {},
    twitter_tweets = {},
    twitter_object = '{}'
    WHERE domain = '{}'
    """.format(retweets, tweets, blob, domain)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return
