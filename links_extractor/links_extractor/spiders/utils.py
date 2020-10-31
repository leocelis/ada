import os
from urllib.parse import urlsplit

# mysql vars
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from utils.conn import get_mysql_conn, dictfecth


def get_all_sites(category: str = None):
    """
    Get all site urls
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_url, sitemap_url FROM scrapy_sites WHERE active = 1
    """

    if category:
        sql += " AND category=%s"

    cursor.execute(sql, category)

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

    # append social networks
    domains.append('facebook.com')
    domains.append('linkedin.com')
    domains.append('twitter.com')
    domains.append('twitch.com')

    print("\nDomain found: {}".format(domains))

    return domains
