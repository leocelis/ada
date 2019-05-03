import os
import sys
import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.conn import get_mysql_conn, dictfecth


def get_all_site_links():
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_link FROM scrapy_sites_links ORDER BY idscrapy_sites_links DESC
    """

    cursor.execute(sql)
    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def save_link_fb_shares(site_link: str, r: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    site_link_title = str(r.get('og_object', {}).get('title', ''))
    fb_shares = int(r.get('share', {}).get('share_count', 0))
    fb_graph_object = ujson.dumps(r)

    sql = """
    INSERT INTO facebook_most_shared(site_link, site_link_title, fb_shares, fb_graph_object)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (site_link, site_link_title, fb_shares, fb_graph_object))
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return

# def check_link_exists(site_link: str) -> bool:
#     conn = get_mysql_conn()
#
#     cursor = conn.cursor()
#
#     r = 0
#     sql = """
#     SELECT site_link FROM scrapy_sites_links WHERE site_link = "{}"
#     """.format(site_link)
#
#     try:
#         r = cursor.execute(sql)
#         conn.commit()
#     except Exception as e:
#         print("\nERROR! ({})".format(str(e)))
#         conn.rollback()
#
#     cursor.close()
#
#     if r > 0:
#         return True
#
#     return False
