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
from joblib import dump
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.getcwd()))
from ada.content_analyzer.utils import get_links_shares
from ada.predictions.utils import lower_case, remove_punctuation, spelling_check, remove_common_words

# ===================================
# DATA CLEANING
# ===================================
dataset = pd.DataFrame(get_links_shares(threshold=10, limit=10))
# dataset = pd.DataFrame(get_links_shares(threshold=10))

# lower case
dataset['link_title'] = dataset['link_title'].apply(lambda x: lower_case(x))

# remove punctuation
dataset['link_title'] = dataset['link_title'].apply(lambda x: remove_punctuation(x))

# spelling check
dataset['link_title'] = dataset['link_title'].apply(lambda x: spelling_check(x))

# remove common words
dataset['link_title'] = dataset['link_title'].apply(lambda x: remove_common_words(x))

# print("Training Dataset")
# print("================")
# print(dataset)

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

# TODO: count how many emotions
# dataset['link_title_sharing_score'] = dataset['emotions_count']

# print("Training Dataset")
# print("================")
# print(dataset)

# ===================================
# VALIDATION
# ===================================

# feature
X = dataset[['link_title_length', 'link_title_words_count', 'link_title_sentiment']]

# target
y = dataset['shares_total']

# training and test dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=100)

# training algorithm
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# save trained model
dump(regressor, 'predictions/link_shares.joblib')

# predict test dataset!
y_pred = regressor.predict(X_test)
df = pd.DataFrame({'Actual Results': y_test, 'Predicted Results': y_pred})
print(df)

exit()

# ===================================
# PREDICTION
# ===================================
new_dataset = pd.DataFrame({'link_title': ['This is a subject test',
                                           'This is a really long subject that you should not read',
                                           'Serverless will kick you in the face']})

# data cleaning
new_dataset['link_title_length'] = new_dataset["link_title"].apply(lambda x: len(x))
new_dataset['link_title_words_count'] = new_dataset["link_title"].apply(lambda x: len(x.split()))
new_dataset['link_title_sentiment'] = 0  # TODO: get sentiment

# predict!
X_new = new_dataset[['link_title_length', 'link_title_words_count', 'link_title_sentiment']]
new_pred = regressor.predict(X_new)
new_dataset['link_shares_prediction'] = new_pred

print("\nPredictions")
print("===========")
print(new_dataset)
print()
