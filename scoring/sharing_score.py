import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import clean_text, get_shares_by_word, get_max_shares

# input title
test_title = "Facebook starts prompting US users to fill out a COVID-19 survey to help track the virus"

# normalize words
test_title_cleaned = clean_text(test_title)
print(test_title_cleaned)

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
max_shares = get_max_shares()  # post title max shares
print("Max {}".format(max_shares))

score = ((s / len(test_title_cleaned)) * 100) / float(max_shares)
print("Score: {}".format(score))

# score_formatted = Decimal(score).quantize(0, ROUND_HALF_UP)
score_formatted = round(score, 2)
print("Score (rounded): {}".format(score_formatted))
