import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import clean_text, get_word_weight


def get_sharing_score(title=None):
    # default score
    final_score = 0

    # normalize words
    title_cleaned = clean_text(title)

    if title_cleaned:
        # sum up words' weight
        s = 0
        for w in title_cleaned:
            c = get_word_weight(w)
            s += c
            print("{} {}".format(w, c))

        score = s * 100
        print("Real score: {}".format(score))

        # adjust score
        if score > 100:
            score = 100

        final_score = round(score, 2)
        print("Score (rounded): {}".format(final_score))

    return final_score


def main():
    get_sharing_score("The Death of Google Search Traffic and What It Means for Marketers")


if __name__ == "__main__":
    main()
