import os
import sys

import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def save_ga_report(title, path, avg_top, top, start_date, users, adsense_clicks, adsense_revenue) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    INSERT INTO ga_reports(page_title, page_path, avg_time_on_page, time_on_page, start_date,
    users, adsense_clicks, adsense_revenue)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("Saving GA report for: {}...\n".format(title))

    try:
        # truncate to 5 decimals
        avg_top = format(float(avg_top), '.5f')
        top = format(float(top), '.5f')
        adsense_clicks = format(float(adsense_clicks), '.5f')
        adsense_revenue = format(float(adsense_revenue), '.5f')

        cursor.execute(sql, (title, path, avg_top, top, start_date, users, adsense_clicks, adsense_revenue))
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def check_ga_report_exists(path: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT page_path FROM ga_reports WHERE page_path = "{}"
    """.format(path)

    try:
        r = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()

    if r > 0:
        return True

    return False


def update_ga_report(avg_top, top, path, users, adsense_clicks, adsense_revenue) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    # truncate to 5 decimals
    avg_top = format(float(avg_top), '.5f')
    top = format(float(top), '.5f')
    adsense_clicks = format(float(adsense_clicks), '.5f')
    adsense_revenue = format(float(adsense_revenue), '.5f')

    sql = """UPDATE ga_reports
    SET avg_time_on_page = {},
    time_on_page = {},
    users = {},
    adsense_clicks = {},
    adsense_revenue = {}
    WHERE page_path = "{}"
    """.format(avg_top, top, users, adsense_clicks, adsense_revenue, path)

    print("Updating GA report for: {}...\n".format(path))

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def get_top_page_time(limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select page_title, avg_time_on_page from ga_reports where users >= 5 and
    page_title NOT like 'Contact me%' and
    page_title NOT like 'Dashboard%' and
    page_title NOT like 'About me%' and
    page_title NOT like 'Home -%'
    order by  avg_time_on_page desc limit 0,{};
    """.format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


# Facebook
def get_fb_shares_by_domain(domain: str, threshold: int = 1, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT site_link, site_link_title, fb_shares FROM facebook_most_shared
    WHERE site_link LIKE "%{}%" AND fb_shares > {} ORDER BY fb_shares
    """.format(domain, threshold)

    if limit > 0:
        sql += " LIMIT 0,{}".format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def check_link_exists(site_link: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT site_link FROM facebook_most_shared WHERE site_link = "{}"
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


def update_link_fb_shares(site_link: str, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    fb_shares = r.get('engagement', {}).get('share_count', 0)
    fb_updated_time = r.get('og_object', {}).get('updated_time', '')
    fb_graph_object = ujson.dumps(r)

    sql = """
    UPDATE facebook_most_shared
    SET fb_shares = {},
    fb_updated_time = '{}',
    fb_graph_object = '{}'
    WHERE site_link = '{}'
    """.format(fb_shares,
               fb_updated_time,
               fb_graph_object.replace("'", r"\'"),
               site_link)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def save_link_fb_shares(site_link: str, r: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    site_link_title = r.get('og_object', {}).get('title', '')
    fb_description = r.get('og_object', {}).get('description', '')
    fb_type = r.get('og_object', {}).get('type', '')
    fb_shares = r.get('engagement', {}).get('share_count', 0)
    fb_updated_time = r.get('og_object', {}).get('updated_time', '')
    fb_graph_object = ujson.dumps(r)

    sql = """
    INSERT INTO facebook_most_shared(site_link, site_link_title, fb_description, fb_type, fb_shares, fb_updated_time,
    fb_graph_object) VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}')
    """.format(site_link,
               site_link_title.replace("'", r"\'"),
               fb_description.replace("'", r"\'"),
               fb_type,
               fb_shares,
               fb_updated_time,
               fb_graph_object.replace("'", r"\'"))

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return


# Domains
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


def get_domains():
    """
    Get all domains

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM domain_stats;
    """

    cursor.execute(sql)
    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def update_domain_fb_shares(domain: str, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    fb_shares = r.get('engagement', {}).get('share_count', 0)
    fb_graph_object = ujson.dumps(r).replace("'", r"\'")

    sql = """
    UPDATE domain_stats
    SET facebook_shares = {},
    fb_object = '{}'
    WHERE domain = '{}'
    """.format(fb_shares, fb_graph_object, domain)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_domain_sharethis_total(domain: str, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    total = int(r.get('total', 0))
    blob = ujson.dumps(r).replace("'", r"\'")

    sql = """
    UPDATE domain_stats
    SET sharethis_total = {},
    sharethis_object = '{}'
    WHERE domain = '{}'
    """.format(total, blob, domain)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_domain_retweets(domain: str, tweets: int, retweets: int, r: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    blob = ujson.dumps(r).replace("'", r"\'")

    sql = """
    UPDATE domain_stats
    SET twitter_retweets = {},
    twitter_tweets = {},
    twitter_object = '{}'
    WHERE domain = '{}'
    """.format(retweets, tweets, blob, domain)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


# ShareThis
def get_sharethis_stats_by_domain(domain: str, threshold: int = 10, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM sharethis_stats
    WHERE site_link LIKE "%{}%" AND total > {} ORDER BY total DESC
    """.format(domain, threshold)

    if limit > 0:
        sql += " LIMIT 0,{}".format(limit)

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


# Twitter

def get_top_tweets(retweet_threshold: int = 5, limit: int = 100):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM twitter_most_retweeted
    WHERE retweet_count > {} ORDER BY retweet_count DESC LIMIT 0,{};
    """.format(retweet_threshold, limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_retweets_by_domain(domain: str, threshold: int = 10, limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT * FROM twitter_most_retweeted
    WHERE query LIKE "%{}%" AND retweet_count > {} ORDER BY retweet_count DESC
    """.format(domain, threshold)

    if limit > 0:
        sql += " LIMIT 0,{}".format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def check_retweet_exists(tweet_id: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT tweet_id FROM twitter_most_retweeted WHERE tweet_id = "{}"
    """.format(tweet_id)

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


def save_link_retweets(query: str, t: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    retweet_count = int(t.get('retweet_count', 0))
    created_at = t['created_at']
    tweet_id = t['id_str']
    tweet = t['text']
    user_id = t['user']['id_str']
    user_name = t['user']['screen_name']
    blob = ujson.dumps(t).replace("'", r"\'")
    tweet_link = "https://twitter.com/{}/status/{}".format(user_name, tweet_id)

    sql = """
    INSERT INTO twitter_most_retweeted(created_at, tweet_id, retweet_count, tweet, user_id, user_name,
    tweet_blob, tweet_link, query)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("\nSaving tweet: {}...".format(tweet_link))

    try:
        cursor.execute(sql, (created_at, tweet_id, retweet_count, tweet, user_id, user_name, blob, tweet_link, query))
        conn.commit()
    except Exception as e:
        print("\nERROR! ({})".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_link_retweets(query: str, t: dict):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    retweet_count = int(t.get('retweet_count', 0))
    tweet_id = t['id_str']
    user_name = t['user']['screen_name']
    blob = ujson.dumps(t).replace("'", r"\'")
    tweet_link = "https://twitter.com/{}/status/{}".format(user_name, tweet_id)

    sql = """
    UPDATE twitter_most_retweeted
    SET retweet_count = {},
    tweet_blob = '{}'
    WHERE tweet_id = '{}'
    """.format(retweet_count, blob, tweet_id)

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def get_title_by_link(link: str):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT title FROM scrapy_sites_links
    WHERE site_link = "{}";
    """.format(link)

    r = cursor.execute(sql)

    if r > 0:
        conn.commit()
        rows = dictfecth(cursor)
        cursor.close()
        title = rows[0]["title"]
        return title
    else:
        cursor.close()
        return ""


# Links shares
def link_shares_update_or_insert(link, title, shares):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    # check if the link exists
    sql = """
    SELECT idlinks_shares FROM links_shares
    WHERE link_url = "{}";
    """.format(link)

    r = cursor.execute(sql)

    if r > 0:
        conn.commit()
        rows = dictfecth(cursor)

        # update shares
        id = rows[0]["idlinks_shares"]
        sql = """
        UPDATE links_shares
        SET shares_total = {}
        WHERE idlinks_shares = '{}'
        """.format(shares, id)

        try:
            cursor.execute(sql)
            print("{} shares updated.".format(link))
            conn.commit()
        except Exception as e:
            print("ERROR! ({})\n".format(str(e)))
            conn.rollback()
            return False

        cursor.close()
        return True
    else:
        # insert new link with shares
        sql = """
        INSERT INTO links_shares(link_url, link_title, shares_total)
        VALUES (%s, %s, %s)
        """.format()

        try:
            cursor.execute(sql, (link, title, shares))
            print("{} shares inserted.".format(link))
            conn.commit()
        except Exception as e:
            print("\nERROR! ({})".format(str(e)))
            conn.rollback()
            return False

        cursor.close()
        return True

    return False
