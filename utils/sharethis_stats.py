import os

import sys
import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_sharethis_stats_by_domain(domain: str, threshold: int = 10, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM sharethis_stats
    WHERE site_link LIKE "%{}%" AND total > {} ORDER BY total DESC LIMIT 0,{};
    """.format(domain, threshold, limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


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
    blob = ujson.dumps(t).replace("'", r"\'")

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
    blob = ujson.dumps(t).replace("'", r"\'")

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
