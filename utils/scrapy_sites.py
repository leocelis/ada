import os
from urllib.parse import urlsplit

import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_all_sites(category: str = None, domain: str = None):
    """
    Get all site urls
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
        sql += " WHERE site_url LIKE '%{}%'".format(domain)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_sites(category: str = None):
    """
    Return domains to crawl
    :return:
    """
    sites = []
    rows = get_all_sites(category=category)

    for r in rows:
        sites.append(r['site_url'])

    print("\nSite found: {}".format(sites))

    return sites


def get_domains(category: str = None):
    """
    Return domains to crawl
    :return:
    """
    domains = []
    rows = get_all_sites(category=category)

    for r in rows:
        splitted_url = urlsplit(r['site_url'])
        domains.append(splitted_url.netloc)

    print("\nDomain found: {}".format(domains))

    return domains
