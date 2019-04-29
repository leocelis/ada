"""
This code was inspired by
https://www.searchenginejournal.com/reorganizing-xml-sitemaps-python/295539/
"""

import re
from collections import Counter
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from wordcloud import WordCloud

nltk.download('stopwords')
# how many words to show in the graph
max_words = 100

# Step 1: Get sitemaps
site = "http://blog.leocelis.com/sitemap_index.xml"

print("Step 1: Retrieving sitemaps for {}\n".format(site))

hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="lxml")
sitemapTags = soup.find_all("sitemap")

print("--> The number of sitemaps are {0}\n".format(len(sitemapTags)))

sitemap_index = {}
for sitemap in sitemapTags:
    sitemap_index[sitemap.findNext("loc").text] = sitemap.findNext("lastmod").text

# Step 2: Pull site urls
print("Step 2: Finding posts sitemaps for {}\n".format(site))

sitemaps = {}
for sitemap_url, lasmod in sitemap_index.items():
    if sitemap_url.find("post") > 0:
        print("--> Posts sitemap found! {}\n".format(sitemap_url))

        req = Request(sitemap_url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, features="lxml")
        URLTags = soup.find_all("url")

        for URL in URLTags:
            link = URL.findNext("loc").text
            print("----> {}\n".format(link))
            sitemaps[link] = URL.findNext("lastmod").text

# Step 3: Load into Pandas dataframe
print("Step 3: loading URLs in Pandas dataframe for {}\n".format(site))
df = pd.DataFrame.from_dict(sitemaps, orient="index", columns=['lastmod'])
df.head(10)

# Step 4: Words frequency count
print("Step 4: counting words for {}\n".format(site))
df["path"] = df.index.map(lambda x: urlparse(x).path)
cnt = Counter()
english_stopwords = set(stopwords.words('english'))

for path in df.path:
    words = re.split("[-/]", path)
    for word in words:
        if len(word) > 0 and word not in english_stopwords and not word.isdigit():
            cnt[word] += 1

cnt.most_common(max_words)

# Step 5: Visualize
print("Step 4: creating words cloud {}\n".format(site))
word_cloud = [x[0] for x in cnt.most_common(max_words)]
word_cloud_obj = WordCloud(max_words=max_words, background_color="white").generate(" ".join(word_cloud))
plt.imshow(word_cloud_obj, interpolation='bilinear')
plt.axis("off")
plt.show()
