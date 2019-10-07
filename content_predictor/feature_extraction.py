from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',
]

X = vectorizer.fit_transform(corpus)

print(X)