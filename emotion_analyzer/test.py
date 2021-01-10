"""
Based on https://github.com/clemtoy/WNAffect
"""
import nltk
from emotion import Emotion
from textblob import TextBlob
from wnaffect import WNAffect

# sentiment
feedbacks = ['giant']

positive_feedbacks = []
negative_feedbacks = []

for feedback in feedbacks:
    feedback_polarity = TextBlob(feedback).sentiment.polarity

    if feedback_polarity > 0:
        positive_feedbacks.append(feedback)
        continue

    negative_feedbacks.append(feedback)

print('Positive_feebacks Count : {}'.format(len(positive_feedbacks)))
print(positive_feedbacks)
print('Negative_feedback Count : {}'.format(len(negative_feedbacks)))
print(negative_feedbacks)
print()
print()
print()
print()

# emotion
wna = WNAffect('emotion_analyzer/wordnet-1.6/', 'emotion_analyzer/wn-domains-3.2/')

# part-of-speech tag
for f in feedbacks:
    ws = f.split(" ")
    for w in ws:
        word = w
        tokens = nltk.word_tokenize(word)
        post_tag = nltk.pos_tag(tokens=tokens)
        print(word)
        print(post_tag[0][1])

        emo = wna.get_emotion(str(word), str(post_tag[0][1]))
        print("Emotion for *{}*: {}".format(word, emo))

        if emo:
            parent = emo.get_level(emo.level - 1)
            print("Parent: {}".format(parent))

            e = Emotion.emotions[str(parent)]
            # print(e.nb_children())
            Emotion.printTree(e)
