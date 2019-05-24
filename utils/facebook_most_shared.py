import os
import sys

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
