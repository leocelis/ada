import os
import sys
from urllib.parse import urlsplit

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_domain(site_url: str):
    splitted_url = urlsplit(site_url)
    d = splitted_url.netloc
    return d.replace("www.", "")


def clean_link(link):
    l = str(link).replace("'", "")
    return l


def is_content_valid(link, title):
    """
    Check for valid links

    :param link:
    :return:
    """
    # at least 3 slashes occurrences
    o = str(link).count('/')
    if o < 3:
        return False

    # at least 30 characters long
    l = len(str(link))
    if l < 30:
        return False

    # at least 15 characters in the title
    t = len(str(title))
    if t < 15:
        return False

    return True


def get_allowed_domains():
    """
    Get all domains
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_url, sitemap_url FROM scrapy_sites
    """

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)

    # extract domains
    domains = list()
    for r in rows:
        d = get_domain(r['site_url'])
        domains.append(d)

    cursor.close()

    return domains
