import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn


def update_link_sharing_score(id, sharing_score=0):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    UPDATE links_shares
    SET sharing_score = {}
    WHERE idlinks_shares = {}
    """.format(sharing_score, id)

    try:
        cursor.execute(sql)
        print("Sharing score for {} updated".format(id))
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()
        return False

    cursor.close()
    return True
