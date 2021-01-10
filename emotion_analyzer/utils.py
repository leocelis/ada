"""
Based on https://github.com/clemtoy/WNAffect
"""
import os
import sys

import nltk
from emotion import Emotion
from wnaffect import WNAffect

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn


def get_word_emotion(word="anger"):
    """
    Return word's emotion and parent emotion

    :param word:
    :return:
    """
    wna = WNAffect('emotion_analyzer/wordnet-1.6/', 'emotion_analyzer/wn-domains-3.2/')
    tokens = nltk.word_tokenize(word)
    post_tag = nltk.pos_tag(tokens=tokens)
    # print(word)
    # print(post_tag[0][1])
    emo = wna.get_emotion(str(word), str(post_tag[0][1]))
    print("Emotion for {}: {}".format(word, emo))

    if emo:
        parent = emo.get_level(emo.level - 1)
        print("Parent: {}".format(parent))

        e = Emotion.emotions[str(parent)]
        # print(e.nb_children()) # print children
        # Emotion.printTree(e) # print emotion tree
        return str(emo), str(parent)

    return


def update_word_emotion(id, emotion, emotion_parent):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    UPDATE prediction_blog_titles
    SET emotion = '{}', emotion_parent = '{}'
    WHERE idprediction_blog_titles = {}
    """.format(emotion, emotion_parent, id)

    try:
        cursor.execute(sql)
        print("emotions updated.")
        conn.commit()
    except Exception as e:
        print("ERROR! ({})\n".format(str(e)))
        conn.rollback()
        return False

    cursor.close()
    return True
