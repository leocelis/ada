"""
Ad Tech News ML Aggregator

Sources:
- MailChimp
- GA
- Twitter
- ShareThis

1. Go to links_extractor/spiders/ada.py, and change category to leocelis
2. Run the spider:
    >cd links_extractor/
    >scrapy crawl ada -o adtech.csv -t csv
3. Import csv to mysql, update utils/csv_to_mysql.py and change csv file
    >python3 utils/csv_to_mysql.py
4. Update content_analzyer/sharethis_to_db.py, with leocelis.com
    >python3 utils/csv_to_mysql.py
5. Update content_analyzer/fb_most_shared.py with leocelis.com
    >python3 content_analyzer/fb_most_shared.py
6. Update content_analyzer/tw_most_retweeted.py with leocelis.com
    >python3 content_analyzer/tw_most_retweeted.py
7. Update content_analyzer/report.py with leolcelis.com
    >python3 content_analyzer/report.py
8. Update config.py with relevant ad tech keywords
9. Pull relevant tweets
    >python content_discovery/twitter_content.py

"""
