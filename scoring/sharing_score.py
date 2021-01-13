import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
from ada.predictions.utils import clean_text, get_word_weight


def get_sharing_score(title=None):
    # default score
    final_score = 0

    # normalize words
    title_cleaned = clean_text(title)

    # for each word, get shares
    s = 0
    for w in title_cleaned:
        c = get_word_weight(w)
        s += c
        print("{} {}".format(w, c))

    if title_cleaned:
        t = s / len(title_cleaned)
        print("Title weight: {}".format(t))

        score = t * 100
        print("Score: {}".format(score))

        # score_formatted = Decimal(score).quantize(0, ROUND_HALF_UP)
        final_score = round(score, 2)
        print("Score (rounded): {}".format(final_score))

    return final_score


def main():
    get_sharing_score("Sofort web")


if __name__ == "__main__":
    main()
