"""
Sync Ad Tech topics
cd links_extractor/ ; time scrapy crawl ada -o adtech.csv -t csv
time python3 utils/csv_to_mysql.py
time python3 content_analyzer/fb_most_shared.py
time python3 content_analyzer/tw_most_retweeted.py
time python3 content_discovery/twitter_content.py
time python3 content_analyzer/sharethis_to_db.py
time python3 content_analyzer/report.py
"""
