import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import clean_text, get_shares_by_word, get_max_shares


def get_sharing_score(title=None):
    # default score
    final_score = 0

    # normalize words
    title_cleaned = clean_text(title)

    # for each word, get shares
    s = 0
    for w in title_cleaned:
        c = get_shares_by_word(w)
        # if 0, remove it
        if c == 0:
            title_cleaned.remove(w)
            continue
        s += c
        print("{} {}".format(w, c))

    # calculate score
    max_shares = get_max_shares()  # post title max shares
    print("Max shares: {}".format(max_shares))

    if title_cleaned:
        title_shares = s / len(title_cleaned)
        print("Title shares: {}".format(title_shares))

        score = (title_shares * 100) / float(max_shares)
        if score >= 100:
            score = 100
        print("Score: {}".format(score))

        # score_formatted = Decimal(score).quantize(0, ROUND_HALF_UP)
        final_score = round(score, 2)
        print("Score (rounded): {}".format(final_score))

    return final_score


def main():
    get_sharing_score("this is a title")


if __name__ == "__main__":
    main()
