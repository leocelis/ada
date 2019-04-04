import os
import sys
from urllib.parse import urlsplit

sys.path.append(os.path.dirname(os.getcwd()))
from conn import get_mysql_conn, dictfecth


def get_all_sites():
    """
    Get all site urls
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_url FROM scrapy_sites
    """

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_sites():
    """
    Return domains to crawl
    :return:
    """
    sites = []
    rows = get_all_sites()

    for r in rows:
        sites.append(r['site_url'])

    print("\nSite found: {}".format(sites))

    return sites


def get_domains():
    """
    Return domains to crawl
    :return:
    """
    domains = []
    rows = get_all_sites()

    for r in rows:
        splitted_url = urlsplit(r['site_url'])
        domains.append(splitted_url.netloc)

    print("\nDomain found: {}".format(domains))

    return domains
