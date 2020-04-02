"""
Data clean up functions

"""
import nltk

from nltk.corpus import stopwords

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
    text = lower_case(text)
    text = remove_punctuation(text)
    text = spelling_check(text)
    text = remove_common_words(text)
    text = lemmatize_text(text)

    return text
