import os
import sys

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
