import os

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
