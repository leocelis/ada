"""

Goal: get the expected open rate of a given email subject

Problem:
What are the main drivers of people openning emails?

- Subject length
- Words used
-

Highlights:
- Avg. open rate is 19% (US)

References:
- https://www.superoffice.com/blog/email-open-rates/

TODOs:

- Create a clean up function

Ideas:
- Collect ad tech blog post titles, and create a wordcloud to use as a training dataset

"""
import os
import sys

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.getcwd()))
from ada.email_analyzer.utils import get_subjects_open_rate
from textblob import TextBlob

# ===================================
# DATA CLEANING
# ===================================
# dataset = pd.read_csv("email_analyzer/subject_training_data.csv", index_col=None) # read from CSV file
dataset = pd.DataFrame(get_subjects_open_rate())

# lower case
dataset['email_subject'] = dataset['email_subject'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# remove punctuation
dataset['email_subject'] = dataset['email_subject'].str.replace('[^\w\s]', '')

# spelling check
dataset['email_subject'] = dataset['email_subject'].apply(
    lambda x: str(TextBlob(x).correct()))  # ===================================
# FEATURE EXTRACTION
# ===================================
# subject length feature
dataset['email_subject_length'] = dataset['email_subject'].apply(lambda x: len(x))

# words count
dataset['email_subject_words_count'] = dataset['email_subject'].apply(lambda x: len(x.split()))

# words used?

print("Training Dataset")
print("================")
print(dataset)
# exit()

# ===================================
# CORRELATION
# ===================================

# correlation matrix
# print("\nCorrelation Matrix")
# print("==================")
# print(dataset.corr())

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

new_dataset['email_subject_length'] = new_dataset["email_subject"].apply(lambda x: len(x))
new_dataset['email_subject_words_count'] = new_dataset["email_subject"].apply(lambda x: len(x.split()))
X_new = new_dataset[['email_subject_length', 'email_subject_words_count']]

# predict!
new_pred = regressor.predict(X_new)
new_dataset['open_rate_pred'] = new_pred

print("\nPredictions")
print("===========")
print(new_dataset)
print()
