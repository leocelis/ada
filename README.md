# Ada Content Performance Analytics

## Installation

```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## ENV VARS

### MySQL
```
export DB_HOST=<val>
export DB_PORT=<val>
export DB_USER=<val>
export DB_PASSWORD=<val>
```

### Twitter
```
export TWITTER_APP_KEY=<val>
export TWITTER_APP_SECRET=<val>
```

### Plotly
```
export PLOTLY_USERNAME=<val>
export PLOTLY_API_KEY=<val>
```

## How to execute scripts

### Facebook Ads Optimization
#### Charts
```
1. Export data from Facebook Ads Reporting and save it in data/
2. python3 fb_ads_optimization/charts.py
3. Check reports/ folder
```

#### Insights
```
1. Export data from Facebook Ads Reporting and save it in data/
2. python3 fb_ads_optimization/insights.py
```

#### Upload graphs to s3 folder
```
1. Create ~/.aws/credentials with
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
2. Create a new s3 folder named "ada-reports"
3. Run python3 fb_ads_optimization/s3_upload.py

```

#### Funnel chart
```
1. Create an account in https://plot.ly/
3. Run python3 fb_ads_optimization/funnel.py
```

### Content Discovery
#### Get most retweeted tweets in Ad Tech
```
1. Create a new database and table
CREATE DATABASE `ada` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;

CREATE TABLE `twitter_most_retweeted` (
  `idtwitter_most_retweeted` int(11) NOT NULL AUTO_INCREMENT,
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `tweet_id` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `tweet_link` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `retweet_count` int(11) DEFAULT NULL,
  `tweet` text COLLATE utf8mb4_bin,
  `user_id` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `user_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `tweet_blob` longtext COLLATE utf8mb4_bin,
  `keyword` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`idtwitter_most_retweeted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

2. Set up config in ada.config 

3. python3 content_discovery/twitter_content.py
```
