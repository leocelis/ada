"""
(c) leocelis.com

Add positive/negative sentiment to each link

Positive = >0
Negative = <0
"""
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_links_shares
from ada.emotion_analyzer.utils import get_sentiment, update_link_sentiment

# get all links shares
links_shares = get_links_shares()

for l in links_shares:
    t = l.get('link_title', "")
    s = get_sentiment(t)

    print("Sentiment for [{}]: {}".format(t, s))
    update_link_sentiment(l.get('idlinks_shares'), s)
