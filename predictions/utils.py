import os
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
    return text.replace('[^\w\s]', '')


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


def clean_all(text):
    """
    Sanitize text

    :param text:
    :return:
    """
    print("Dirty {}".format(text))
    text = lower_case(text)
    text = remove_punctuation(text)
    # text = spelling_check(text)
    # text = remove_common_words(text)
    text = lemmatize_text(text)
    print("Cleaned {}".format(text))

    return text


def words_value(words, df, shares_field):
    """
    Add shares per word

    :param df:
    :param words:
    :param shares_field:
    :return: dict
    """
    for index, row in df.iterrows():
        for w in row["site_link_title"]:
            if w in words:
                words[w] += row[shares_field]
            else:
                words[w] = row[shares_field]

            print("{} {}".format(w, words[w]))

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


def get_words_shares():
    """
    Get words and shares

    :return:
    """
    conn = get_mysql_conn()
    cursor = conn.cursor()

    sql = """
    select word, shares from prediction_blog_titles
    """

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
