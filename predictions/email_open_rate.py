"""
(c) leocelis.com

Predicts Email Open Rate

Source: MailChimp

Features:
- Subject length
- Words count
- Words value (*)

Target:
- Open rate

(*) Assumption: subject lines that use most-shared words will have a higher open rate

TODO: add how efficient is the ml algo
"""
import os
import sys

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.getcwd()))
from ada.email_analyzer.utils import get_subjects_open_rate

from ada.predictions.utils import lower_case, remove_punctuation, spelling_check, remove_common_words

# ===================================
# DATA CLEANING
# ===================================
dataset = pd.DataFrame(get_subjects_open_rate())

# lower case
dataset['email_subject'] = dataset['email_subject'].apply(lambda x: lower_case(x))

# remove punctuation
# dataset['email_subject'] = dataset['email_subject'].str.replace('[^\w\s]', '')
dataset['email_subject'] = dataset['email_subject'].apply(lambda x: remove_punctuation(x))

# spelling check
dataset['email_subject'] = dataset['email_subject'].apply(lambda x: spelling_check(x))

# remove common words

dataset['email_subject'] = dataset['email_subject'].apply(lambda x: remove_common_words(x))

# word shares
# TODO: take each word, get the shares value, sum all the words values to create a new feature
#
# print("Training Dataset")
# print("================")
# print(dataset)
# exit()

# ===================================
# FEATURE EXTRACTION
# ===================================
# subject length feature
dataset['email_subject_length'] = dataset['email_subject'].apply(lambda x: len(x))

# words count
dataset['email_subject_words_count'] = dataset['email_subject'].apply(lambda x: len(x.split()))

# print("Training Dataset")
# print("================")
# print(dataset)
# exit()

# ===================================
# PREDICTION
# ===================================

# feature
X = dataset[['email_subject_length', 'email_subject_words_count']]

# target
y = dataset['open_rate']

# training and test dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=100)

# training algorithm
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# predict test dataset!
y_pred = regressor.predict(X_test)
df = pd.DataFrame({'Actual Results': y_test, 'Predicted Results': y_pred})

# predict new dataset
new_dataset = pd.DataFrame({'email_subject': ['This is a subject test',
                                              'This is a really long subject that you should not read',
                                              'creative performance dashboards are broken',
                                              'How about this super long and boring subject line?',
                                              'facebook ad library',
                                              'chat beats email',
                                              'abc is for you!',
                                              'a b c']})

# data cleaning
new_dataset['email_subject_length'] = new_dataset["email_subject"].apply(lambda x: len(x))
new_dataset['email_subject_words_count'] = new_dataset["email_subject"].apply(lambda x: len(x.split()))

# predict!
X_new = new_dataset[['email_subject_length', 'email_subject_words_count']]
new_pred = regressor.predict(X_new)
new_dataset['open_rate_pred'] = new_pred

print("\nPredictions")
print("===========")
print(new_dataset)
print()
