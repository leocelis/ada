import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# dataset
dataset = pd.read_csv("email_analyzer/subject_training_data.csv", index_col=None)

# subject length feature
dataset['email_subject_length'] = dataset["email_subject"].apply(lambda x: len(x))
# print("Training Dataset")
# print("================")
# print(dataset)

# ===================================
# CORRELATION
# ===================================

# correlation matrix
print("\nCorrelation Matrix")
print("==================")
print(dataset.corr())

# ===================================
# PREDICTION
# ===================================

# feature
X = dataset[['email_subject_length']]

# target
y = dataset['open_rate']

# training and test dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

# training algorithm
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# predict test dataset!
y_pred = regressor.predict(X_test)
df = pd.DataFrame({'Actual Results': y_test, 'Predicted Results': y_pred})

# predict new dataset
new_dataset = pd.DataFrame({'email_subject': ['This is a subject test',
                                              'This is a really long subject that you should not read',
                                              'Too short',
                                              'A',
                                              '',
                                              'How about this super long and boring subject line?']})
new_dataset['email_subject_length'] = new_dataset["email_subject"].apply(lambda x: len(x))
X_new = new_dataset[['email_subject_length']]
new_pred = regressor.predict(X_new)
new_dataset['open_rate_pred'] = new_pred

print("\nPredictions")
print("===========")
print(new_dataset)
print()
