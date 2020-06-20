import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import clean_all, get_shares_by_word, get_max_shares

# input title
test_title = "MailChimp is Amazing"

# normalize words
test_title_cleaned = clean_all(test_title)
print(test_title_cleaned)

# for each word, get shares
s = 0
for w in test_title_cleaned:
    c = get_shares_by_word(w)
    s += c
    print("{} {}".format(w, c))

# calculate score
max_shares = get_max_shares()
print("Max {}".format(max_shares))

score = ((s / len(test_title_cleaned)) * 100) / float(max_shares)
print("Score: {}".format(score))

score_formatted = Decimal(score).quantize(0, ROUND_HALF_UP)
print("Score (rounded): {}".format(score_formatted))
