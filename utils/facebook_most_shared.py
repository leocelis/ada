import os
import sys

import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_fb_shares_by_domain(domain: str, threshold: int = 1, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_link, site_link_title, fb_shares FROM facebook_most_shared
    WHERE site_link LIKE "%{}%" AND fb_shares > {} ORDER BY fb_shares DESC LIMIT 0,{};
    """.format(domain, threshold, limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


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
