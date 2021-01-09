import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import get_words_shares
from ada.emotion_analyzer.utils import get_word_emotion, update_word_emotion

# get all the words
words = get_words_shares()

for w in words:
    # get the emotion
    emotions = get_word_emotion(w.get('word'))

    # save the emotion
    if emotions:
        update_word_emotion(w.get('idprediction_blog_titles'),
                            emotions[0],
                            emotions[1])
