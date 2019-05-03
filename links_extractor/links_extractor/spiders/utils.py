import os
from urllib.parse import urlsplit

import pymysql

# mysql vars
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def get_mysql_conn():
    """
    Get MySQL connection object
    :return:
    """
    # if if set up already, return it
    # global gmysql_conn
    # if gmysql_conn:
    #    return get_mysql_conn

    # connect to the server
    gmysql_conn = pymysql.connect(host=DB_HOST,
                                  port=int(DB_PORT),
                                  user=DB_USER,
                                  passwd=DB_PASSWORD,
                                  db="ada",
                                  connect_timeout=30,
                                  use_unicode=True)
    return gmysql_conn


def dictfecth(cursor):
    """
    Convert cursor to dict

    :param cursor:
    :return:
    """
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def get_all_sites():
    """
    Get all site urls
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_url, sitemap_url FROM scrapy_sites HAVING sitemap_url IS NULL
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
