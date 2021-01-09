"""
Based on https://github.com/clemtoy/WNAffect
"""
import nltk
from emotion import Emotion
from textblob import TextBlob
from wnaffect import WNAffect

# sentiment
feedbacks = ['Serverless will kick you in the face',
             "Targeted Ads",
             "Brand Equity",
             "How to avoid the one million-dollar mistake using Amazon Web Services",
             'Integration design in a serverless world',
             'has donated exactly $0',
             'Trump Moved $2.7 Million Of Campaign-Donor Money Into His Business Before Election Day',
             'Periodic Table of SEO Factors',
             'The U.N. Says America Is Already Cutting So Much Carbon It Doesn’t Need The Paris Climate Accord',
             'A New Variant Of Covid-19 Has Emerged In England - Here Is What It Could Mean For The Pandemic And Vaccines',
             'Inside Kylie Jenner’s Web of Lies—and Why She’s No Longer a Billionaire',
             'Amazon LumberyardA free cross-platform 3D game engine, with Full Source, integrated with AWS and Twitch',
             'Republicans Block Trump, Democrats’ Bid To Increase Stimulus Checks To $2,000']

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
