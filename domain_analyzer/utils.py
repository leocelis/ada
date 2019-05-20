import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_all_sitemaps(category: str = None, domain: str = None):
    """
    Get all the sitemaps
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_url, sitemap_url FROM scrapy_sites
    """

    if category:
        sql += " WHERE category='{}'".format(category)

    if domain:
        if "WHERE" in sql:
            sql += " AND site_url LIKE '%{}%'".format(domain)
        else:
            sql += " WHERE site_url LIKE '%{}%'".format(domain)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def save_site_link(site_url: str, site_link: str, title: str = "", lastmod: str = None) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    # current time
    if not lastmod:
        lastmod = str(datetime.utcnow())

    sql = """
    INSERT INTO scrapy_sites_links(site_url, site_link, title, lastmod)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (site_url, site_link, title, lastmod))
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
    SELECT site_link FROM scrapy_sites_links WHERE site_link = "{}"
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
