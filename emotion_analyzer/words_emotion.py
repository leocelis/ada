import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.emotion_analyzer.utils import get_word_emotion, update_word_emotion, get_words_wo_emotion

# get all the words
words = get_words_wo_emotion()

for w in words:
    word = str(w.get('word'))
    print("Finding emotion for {}".format(word))

    # get the emotion
    emotions = get_word_emotion(word)

    # save the emotion
    if emotions:
        update_word_emotion(w.get('idprediction_blog_titles'),
                            emotions[0],
                            emotions[1])
