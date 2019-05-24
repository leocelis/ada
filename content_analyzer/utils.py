import os
import sys

import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_site_links_by_category(category: str):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = "SELECT A.site_link as site_link FROM scrapy_sites_links as A " \
          "INNER JOIN scrapy_sites as B ON A.site_url = B.site_url " \
          "WHERE B.category = '{}'".format(category)

    cursor.execute(sql)
    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


# Facebook
def save_link_fb_shares(site_link: str, r: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    site_link_title = r.get('og_object', {}).get('title', '')
    fb_description = r.get('og_object', {}).get('description', '')
    fb_type = r.get('og_object', {}).get('type', '')
    fb_shares = r.get('engagement', {}).get('share_count', 0)
    fb_updated_time = r.get('og_object', {}).get('updated_time', '')
    fb_graph_object = ujson.dumps(r)

    sql = """
    INSERT INTO facebook_most_shared(site_link, site_link_title, fb_description, fb_type, fb_shares, fb_updated_time,
    fb_graph_object) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (site_link, site_link_title, fb_description, fb_type, fb_shares, fb_updated_time,
                             fb_graph_object))
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def check_link_exists(site_link: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT site_link FROM facebook_most_shared WHERE site_link = "{}"
    """.format(site_link)

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


def update_link_fb_shares(site_link: str, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    fb_shares = r.get('engagement', {}).get('share_count', 0)
    fb_updated_time = r.get('og_object', {}).get('updated_time', '')
    fb_graph_object = ujson.dumps(r)

    sql = """
    UPDATE facebook_most_shared
    SET fb_shares = {},
    fb_updated_time = '{}',
    fb_graph_object = '{}'
    WHERE site_link = '{}'
    """.format(fb_shares, fb_updated_time, fb_graph_object, site_link)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


# Twitter
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


# ShareThis
def check_link_stats(site_link: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT site_link FROM sharethis_stats WHERE site_link = "{}"
    """.format(site_link)

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


def save_link_stats(link: str, t: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    total = int(t.get('total', 0))
    blob = ujson.dumps(t)

    sql = """
    INSERT INTO sharethis_stats(site_link, total, response_blob)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (link, total, blob))
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_link_stats(link: str, t: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    total = int(t.get('total', 0))
    blob = ujson.dumps(t)

    sql = """
    UPDATE sharethis_stats
    SET total = {},
    response_blob = '{}'
    WHERE site_link = '{}'
    """.format(total, blob, blob)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return
