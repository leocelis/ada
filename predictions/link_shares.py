"""
(c) leocelis.com

Predicts Link Shares based on given Link's Title

Features:
- Title length
- Words count
- Sentiment

Pending features:
- Word emotion

Target:
- Shares
"""
import os
import sys

import pandas as pd
from joblib import dump, load
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_links_shares
from ada.predictions.utils import lower_case, remove_punctuation, remove_common_words
from ada.emotion_analyzer.utils import get_sentiment
from ada.scoring.sharing_score import get_sharing_score

# show all columns
pd.set_option('display.max_columns', None)

# load trained model
try:
    regressor = load('predictions/link_shares.joblib')
except:
    print("Trained model not found!\n\n\n")
    # ===================================
    # DATA CLEANING
    # ===================================
    #dataset = pd.DataFrame(get_links_shares(threshold=0, limit=20000))
    dataset = pd.DataFrame(get_links_shares(threshold=1))
    #dataset = pd.DataFrame(get_links_shares())

    # lower case
    dataset['link_title'] = dataset['link_title'].apply(lambda x: lower_case(x))

    # remove punctuation
    dataset['link_title'] = dataset['link_title'].apply(lambda x: remove_punctuation(x))

    # spelling check
    # dataset['link_title'] = dataset['link_title'].apply(lambda x: spelling_check(x))

    # remove common words
    dataset['link_title'] = dataset['link_title'].apply(lambda x: remove_common_words(x))

    print("Training Dataset")
    print("================")
    print(dataset)

    # ===================================
    # FEATURE EXTRACTION
    # ===================================
    # subject length feature
    dataset['link_title_length'] = dataset['link_title'].apply(lambda x: len(x))

    # words count
    dataset['link_title_words_count'] = dataset['link_title'].apply(lambda x: len(x.split()))

    # sentiment
    dataset['link_title_sentiment'] = dataset['sentiment']

    # sharing score
    dataset['link_title_sharing_score'] = dataset['sharing_score']

    # shares total
    # dataset['link_title_shares_total'] = dataset['shares_total']

    # TODO: count how many emotions
    # dataset['link_title_sharing_score'] = dataset['emotions_count']

    print("Training Dataset")
    print("================")
    print(dataset)

    # ===================================
    # VALIDATION
    # ===================================

    # feature
    X = dataset[['link_title_length',
                 'link_title_words_count',
                 'link_title_sentiment',
                 'link_title_sharing_score']]
    # 'link_title_shares_total']]

    # target
    y = dataset['shares_total']
    # y = dataset['sharing_score']

    # training and test dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=140)

    # training algorithm
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    dump(regressor, 'predictions/link_shares.joblib')

    # predict test dataset!
    y_pred = regressor.predict(X_test)
    df = pd.DataFrame({'Actual Results': y_test, 'Predicted Results': y_pred})
    print(df)

    # accuracy
    accuracy = regressor.score(X_test, y_test)
    print('\n\nAccuracy: {} \n\n'.format(accuracy))
    exit()

# ===================================
# PREDICTION
# ===================================
new_dataset = pd.DataFrame({'link_title': ['Sofort integration guide',
                                           'Serverless will kick you in the face',
                                           'Social Media Marketing World 2021',
                                           'huge work-from-home experiment',
                                           'Click here to return to Amazon Web Services homepage']})

# data cleaning
new_dataset['link_title_length'] = new_dataset["link_title"].apply(lambda x: len(x))
new_dataset['link_title_words_count'] = new_dataset["link_title"].apply(lambda x: len(x.split()))
new_dataset['link_title_sentiment'] = new_dataset["link_title"].apply(lambda x: get_sentiment(x))
new_dataset['link_title_sharing_score'] = new_dataset["link_title"].apply(lambda x: get_sharing_score(x))

# predict!
X_new = new_dataset[['link_title_length',
                     'link_title_words_count',
                     'link_title_sentiment',
                     'link_title_sharing_score']]
new_pred = regressor.predict(X_new)
new_dataset['link_shares_prediction'] = new_pred

print("\nPredictions")
print("===========")
print(new_dataset)
print()
