"""
(c) leocelis.com

Add the sharing score for each link
"""
import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_links_shares
from ada.scoring.sharing_score import get_sharing_score
from ada.scoring.utils import update_link_sharing_score

# get all links shares
links_shares = get_links_shares()

for l in links_shares:
    t = l.get('link_title', "")
    s = get_sharing_score(t)

    print("Sharing score for [{}]: {}".format(t, s))
    update_link_sharing_score(l.get('idlinks_shares'), s)
