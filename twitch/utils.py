# TODO: Add output of new top streamers, new top game, with stats (as they were tweets)
# TODO: setup cronjob in nearly real-time (check rate limits)

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth


def get_top_game_last_entry(game_id):
    """
    Get the last stats for a given game

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT current_position FROM twitch_top_games
    WHERE game_id = "{}"
    ORDER BY insert_time DESC
    LIMIT 0,1
    """.format(game_id)
    print(sql)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    if rows:
        return rows[0]

    return False


def insert_top_game_stats(r, current_position, last_position):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    game_id = r.get('id', 0)
    game_name = r.get('name', "")
    box_art_url = r.get('box_art_url', "")
    # current_position = r.get('current_position', "")
    # last_position = r.get('last_position', "")
    delta_position = int(last_position) - int(current_position)

    sql = """
    INSERT INTO twitch_top_games(game_id, game_name, box_art_url, current_position, last_position, delta_position)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (game_id, game_name, box_art_url, current_position, last_position, delta_position))
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def get_top_stream_last_entry(stream_id):
    """
    Get the last stats for a given stream

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT viewer_count FROM twitch_top_streams
    WHERE stream_id = "{}"
    ORDER BY insert_time DESC
    LIMIT 0,1
    """.format(stream_id)
    print(sql)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    if rows:
        return rows[0]

    return False


def insert_top_stream_stats(r, last_viewer_count):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    stream_id = r.get('id')
    user_id = r.get('user_id', "")
    user_name = r.get('user_name', "")
    game_id = r.get('game_id', "")
    stream_type = r.get('type', "")
    stream_title = r.get('title', "")
    viewer_count = r.get('viewer_count', 0)
    started_at = r.get('started_at', "")
    stream_language = r.get('language', "")
    thumbnail_url = r.get('thumbnail_url', "")
    tag_ids = str(r.get('tag_ids', ""))
    prev_viewer_count = last_viewer_count
    delta_viewer_count = int(last_viewer_count) - int(viewer_count)

    sql = """
    INSERT INTO twitch_top_streams(stream_id, user_id, user_name, game_id, stream_type, stream_title, viewer_count, started_at, stream_language, thumbnail_url, tag_ids, prev_viewer_count, delta_viewer_count)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (
            stream_id, user_id, user_name, game_id, stream_type, stream_title, viewer_count, started_at,
            stream_language, thumbnail_url, tag_ids, prev_viewer_count, delta_viewer_count))
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()

    cursor.close()
    return


def get_top_streamer():
    """
    Get the top streamer with most concurrent-viwers

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT user_name, viewer_count FROM twitch_top_streams ORDER BY viewer_count DESC LIMIT 0,1;
    """

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    if rows:
        return rows[0]['user_name'], rows[0]['viewer_count']

    return 0


def get_top_game():
    """
    Get the game with most times in the Top 1 position

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT COUNT(*) as count_number, game_name FROM ada.twitch_top_games WHERE current_position = 1
    GROUP BY game_name ORDER BY count_number DESC LIMIT 0,5;
    """

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    if rows:
        return rows[0]['game_name']

    return ""
