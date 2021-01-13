import os
import string
import sys

import nltk
from nltk.corpus import stopwords

sys.path.append(os.path.dirname(os.getcwd()))
from ada.utils.conn import get_mysql_conn, dictfecth

nltk.download('wordnet')

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()
from textblob import TextBlob


def lower_case(text):
    return " ".join(text.lower() for text in text.split())


def remove_punctuation(text):
    # return text.replace('[^\w\s]', '').replace('"', '')
    s = text.translate(str.maketrans('', '', string.punctuation))
    return s


def spelling_check(text):
    return str(TextBlob(text).correct())


def remove_common_words(text):
    stop = stopwords.words('english')
    return ' '.join([word for word in text.split() if word not in stop])


def lemmatize_text(text):
    """
    Return root word

    :param text: string
    :return: string
    """
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]


def clean_text(text):
    """
    Sanitize text

    :param text:
    :return:
    """
    print("Dirty: '{}'".format(text))
    text = lower_case(text)
    text = remove_punctuation(text)
    # text = spelling_check(text)
    text = remove_common_words(text)
    text = lemmatize_text(text)
    print("Cleaned: {}".format(text))

    return text


def words_shares(df):
    """
    Take the highest shares and assing it to a word

    :param df:
    :param words:
    :param shares_field:
    :return: dict
    """
    words = dict()

    for index, row in df.iterrows():
        for w in row["link_title"]:
            # if the word is in the dic already
            if w in words:
                # if the shares are greater than stored
                if row["shares_total"] > words[w]:
                    words[w] = row["shares_total"]
            else:
                words[w] = row["shares_total"]

            print("Word {} - {} shares".format(w, words[w]))

    return words


def words_weight(df):
    """
    Calculates the words weight
    """
    words = dict()
    m = get_max_shares()

    for index, row in df.iterrows():
        for w in row["link_title"]:
            s = row["shares_total"]
            weight = s / m

            # if the word is in the title
            if w in words:
                if weight > words[w]:
                    words[w] = w
            else:
                words[w] = weight

            print("Word {} weight: {}".format(w, words[w]))

    return words


def word_shares_upsert(word, shares):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    # check if the word exists
    sql = """
    SELECT idprediction_blog_titles FROM prediction_blog_titles
    WHERE word = "{}";
    """.format(word)

    r = cursor.execute(sql)

    if r > 0:
        conn.commit()
        rows = dictfecth(cursor)

        # update shares
        id = rows[0]["idprediction_blog_titles"]
        sql = """
        UPDATE prediction_blog_titles
        SET shares = {}
        WHERE idprediction_blog_titles = '{}'
        """.format(shares, id)

        try:
            cursor.execute(sql)
            print("{} = {} shares updated.".format(word, shares))
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
        INSERT INTO prediction_blog_titles(word, shares)
        VALUES (%s, %s)
        """.format()

        try:
            cursor.execute(sql, (word, shares))
            print("{} = {} shares inserted.".format(word, shares))
            conn.commit()
        except Exception as e:
            print("\nERROR! ({})".format(str(e)))
            conn.rollback()
            return False

        cursor.close()
        return True


def word_weight_upsert(word, weight):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    # check if the word exists
    sql = """
    SELECT idprediction_blog_titles FROM prediction_blog_titles
    WHERE word = "{}";
    """.format(word)

    r = cursor.execute(sql)

    if r > 0:
        conn.commit()
        rows = dictfecth(cursor)

        # update shares
        id = rows[0]["idprediction_blog_titles"]
        sql = """
        UPDATE prediction_blog_titles
        SET weight = {}
        WHERE idprediction_blog_titles = '{}'
        """.format(weight, id)

        try:
            cursor.execute(sql)
            print("{} = {} weight updated.".format(word, weight))
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
        INSERT INTO prediction_blog_titles(word, weight)
        VALUES (%s, %s)
        """.format()

        try:
            cursor.execute(sql, (word, weight))
            print("{} = {} weight inserted.".format(word, weight))
            conn.commit()
        except Exception as e:
            print("\nERROR! ({})".format(str(e)))
            conn.rollback()
            return False

        cursor.close()
        return True


def get_words_shares(limit=0):
    """
    Get words and shares

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select idprediction_blog_titles, word, shares from prediction_blog_titles
    """

    if limit:
        sql += " ORDER BY shares desc LIMIT 0,{}".format(limit)

    cursor.execute(sql)

    conn.commit()
    rows = dictfecth(cursor)
    cursor.close()

    return rows


def get_shares_by_word(word):
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select shares from prediction_blog_titles
    WHERE word = "{}";
    """.format(word)

    r = cursor.execute(sql)

    if r > 0:
        conn.commit()
        rows = dictfecth(cursor)

        return rows[0]["shares"]

    return 0


def get_max_shares():
    """
    Get post with max shares
    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    SELECT MAX(shares_total) as max_shares FROM links_shares
    """

    r = cursor.execute(sql)

    if r > 0:
        conn.commit()
        rows = dictfecth(cursor)

        return rows[0]["max_shares"]

    return 0
