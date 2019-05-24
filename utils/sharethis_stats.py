import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_sharethis_stats_by_domain(domain: str, threshold: int = 10, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_link, total FROM sharethis_stats
    WHERE site_link LIKE "%{}%" AND total > {} ORDER BY total DESC LIMIT 0,{};
    """.format(domain, threshold, limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows
