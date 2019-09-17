import os

import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_links_count(site_url: str):
    """
    How many links per domain

    :param site_url:
    :return:
    """
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


def get_all_site_links(domain: str = None, keyword: str = None, limit: int = None):
    """
    Get all links for a given domain

    :param domain:
    :param keyword:
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    select = "SELECT site_link FROM scrapy_sites_links"

    where = None
    if domain:
        where = "WHERE site_url like '%{}%' ".format(domain)

    if keyword:
        if not where:
            where = "WHERE site_link like '%{}%'".format(keyword)
        else:
            where += "AND site_link like '%{}%'".format(keyword)

    order = "ORDER BY idscrapy_sites_links DESC "

    if limit:
        limit = "LIMIT 0,{}".format(limit)
    else:
        limit = ""

    sql = "{} {} {} {}".format(select, where, order, limit)

    cursor.execute(sql)
    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_site_links_by_category(category: str):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = "SELECT A.site_link as site_link FROM scrapy_sites_links as A " \
          "INNER JOIN scrapy_sites as B ON A.site_url = B.site_url " \
          "WHERE B.category = '{}'".format(category)

    cursor.execute(sql)
    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows
