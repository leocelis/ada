import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import clean_text, get_shares_by_word, get_max_shares

# input title
test_title = "Why is Ad Tech important?"

# normalize words
test_title_cleaned = clean_text(test_title)

# for each word, get shares
s = 0
for w in test_title_cleaned:
    c = get_shares_by_word(w)
    # if 0, remove it
    if c == 0:
        test_title_cleaned.remove(w)
        continue
    s += c
    print("{} {}".format(w, c))

# calculate score
print("---------------")
max_shares = get_max_shares()  # post title max shares
print("Max shares: {}".format(max_shares))

title_shares = s / len(test_title_cleaned)
print("Title shares: {}".format(title_shares))

score = (title_shares * 100) / float(max_shares)
if score >= 100:
    score = 100
print("Score: {}".format(score))

# score_formatted = Decimal(score).quantize(0, ROUND_HALF_UP)
score_formatted = round(score, 2)
print("Score (rounded): {}".format(score_formatted))
