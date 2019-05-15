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
    open_rate = r.get('opens', {}).get('open_rate', 0)
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


def update_campaign_report(email_subject: str, r: dict) -> None:
    conn = get_mysql_conn()
    cursor = conn.cursor()

    emails_sent = r.get('emails_sent', 0)
    unique_opens = r.get('opens', {}).get('unique_opens', 0)
    open_rate = r.get('opens', {}).get('open_rate', 0)
    response_object = ujson.dumps(r)

    sql = """
    UPDATE mailchimp_reports
    SET unique_opens = %s,
    open_rate = %s,
    emails_sent = %s,
    response_object = "%s"
    WHERE email_subject = "%s"
    """

    print("Updating report for: {}...\n".format(email_subject))

    try:
        cursor.execute(sql, (unique_opens, open_rate, emails_sent, response_object, email_subject))
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
    select * from mailchimp_reports where emails_sent > 100 order by unique_opens desc limit 0,{};
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
    select * from mailchimp_reports where emails_sent > 100 order by open_rate desc limit 0,{};
    """.format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows
