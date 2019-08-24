"""
NLP

Sentiment analysis
Predictions / Classification
"""
import urllib.request

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# pull text
response = urllib.request.urlopen('https://en.wikipedia.org/wiki/SpaceX')
html = response.read()

# clean text
soup = BeautifulSoup(html, 'html5lib')
text = soup.get_text(strip=True)

# convert to tokens
tokens = [t for t in text.split()]
# print(tokens)

# plot count words
sr = stopwords.words('english')
clean_tokens = tokens[:]

for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token)

freq = nltk.FreqDist(clean_tokens)

# print chart
for key, val in freq.items():
    print(str(key) + ':' + str(val))

freq.plot(20, cumulative=False)
