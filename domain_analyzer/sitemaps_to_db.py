import os
import sys
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.getcwd()))
from ada.domain_analyzer.utils import get_all_sitemaps, check_link_exists, save_site_link

hdr = {'User-Agent': 'Mozilla/5.0'}

# Get all sitemaps
sitemaps_urls = get_all_sitemaps(category='rent')
# sitemaps_urls = get_all_sitemaps()

sitemaps_collected = {}

for sm in sitemaps_urls:
    sm_url = sm.get('sitemap_url')
    site_url = sm['site_url']

    if sm_url:
        print("Pulling links for {}\n".format(sm_url))

        try:
            # get sitemaps
            req = Request(sm_url, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, features="lxml")
            sitemapTags = soup.find_all("sitemap")

            print("--> The number of sitemaps are {}\n".format(len(sitemapTags)))

            # create index with all sitemaps
            sitemap_index = {}
            for sitemap in sitemapTags:
                sitemap_index[sitemap.findNext("loc").text] = sitemap.findNext("lastmod").text

            # for each sitemap, pull links
            sitemaps = {}
            for sitemap_url, lasmod in sitemap_index.items():
                req = Request(sitemap_url, headers=hdr)
                page = urlopen(req)
                soup = BeautifulSoup(page, features="lxml")
                URLTags = soup.find_all("url")

                for URL in URLTags:
                    link = URL.findNext("loc").text
                    lastmod = URL.findNext("lastmod").text

                    print("----> Saving {}\n".format(link))

                    # save link if it doesn't exist
                    if not check_link_exists(link):
                        save_site_link(site_url, link, lastmod)

        except Exception as e:
            print("[ERROR] {}".format(str(e)))
            pass
