import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_links_count(site_url: str):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT COUNT(*) as count FROM scrapy_sites_links WHERE site_url = %s;
    """

    cursor.execute(sql, site_url)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    count = rows[0].get('count', 0)

    return count
