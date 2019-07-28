import os
import sys

import ujson

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def save_campaign_report(r: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    email_subject = r.get('subject_line', 'No subject')
    emails_sent = r.get('emails_sent', 0)
    unique_opens = r.get('opens', {}).get('unique_opens', 0)
    open_rate = round(r.get('opens', {}).get('open_rate', 0) * 100, 2)
    response_object = ujson.dumps(r)

    sql = """
    INSERT INTO mailchimp_reports(email_subject, emails_sent, unique_opens, open_rate, response_object)
    VALUES (%s, %s, %s, %s, %s)
    """

    print("Saving report for: {}...\n".format(email_subject))

    try:
        cursor.execute(sql, (email_subject, emails_sent, unique_opens, open_rate, response_object))
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def save_member(item: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    city = item.get('merge_fields', {}).get('FCITY')
    role = item.get('merge_fields', {}).get('FROLE')
    country_code = item.get('location', {}).get('country_code')
    name = item.get('merge_fields', {}).get('FNAME')
    email = item.get('email_address')
    rating = item.get('member_rating', 0)
    open_rate = item.get('stats', {}).get('avg_open_rate', 0)
    click_rate = item.get('stats', {}).get('avg_click_rate', 0)

    sql = """
    INSERT INTO mailchimp_members(name, email, country_code, city, role, rating, open_rate, click_rate)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("Saving member: {}...\n".format(name))

    try:
        cursor.execute(sql, (name, email, country_code, city, role, rating, open_rate, click_rate))
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def check_report_exists(email_subject: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT email_subject FROM mailchimp_reports WHERE email_subject = "{}"
    """.format(email_subject)

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


def check_member_exists(email: str) -> bool:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    r = 0
    sql = """
    SELECT email FROM mailchimp_members WHERE email = "{}"
    """.format(email)

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


def update_campaign_report(email_subject: str, r: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    emails_sent = r.get('emails_sent', 0)
    unique_opens = r.get('opens', {}).get('unique_opens', 0)
    open_rate = round(r.get('opens', {}).get('open_rate', 0) * 100, 2)
    response_object = ujson.dumps(r)

    sql = """UPDATE mailchimp_reports 
    SET unique_opens = {},
    open_rate = {},
    emails_sent = {},
    response_object = '{}' 
    WHERE email_subject = "{}"
    """.format(unique_opens, open_rate, emails_sent, response_object, email_subject)

    print("Updating report for: {}...\n".format(email_subject))

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def update_member(email: str, item: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    rating = item.get('member_rating', 0)
    open_rate = item.get('stats', {}).get('avg_open_rate', 0)
    click_rate = item.get('stats', {}).get('avg_click_rate', 0)

    sql = """UPDATE mailchimp_members
    SET rating = {},
    open_rate = {},
    click_rate = {}
    WHERE email = "{}"
    """.format(rating, open_rate, click_rate, email)

    print("Updating member: {}...\n".format(email))

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def get_top_opens(limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select email_subject, unique_opens, open_rate, emails_sent
    from mailchimp_reports where emails_sent > 100 order by unique_opens desc limit 0,{};
    """.format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_top_open_rate(limit: int = 10):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select email_subject, unique_opens, open_rate, emails_sent
    from mailchimp_reports where emails_sent > 100 order by open_rate desc limit 0,{};
    """.format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_members_by_country():
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT country_code as country, COUNT(*) as total
    from mailchimp_members WHERE country_code <> '' GROUP BY country_code;
    """

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_engagement_by_country():
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select country_code as country, (SUM(open_rate) + SUM(click_rate)) as total
    from mailchimp_members WHERE country_code <> '' GROUP BY country_code ;
    """

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows
