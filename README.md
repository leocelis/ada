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

## How to execute scripts

### Facebook Ads Optimization
#### Charts
```

Required fields from Facebook Ads Reporting:

Country analysis: Country, Results, Amount Spent (USD), Cost per Result, Cost per 1,000 People Reached

Save as country.csv
python3 fb_ads_optimization/charts.py # generate charts
python3 fb_ads_optimization/insights.py # get insights
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
2. Export env vars:
export PLOTLY_USERNAME=<val>
export PLOTLY_API_KEY=<val>
3. Run python3 fb_ads_optimization/funnel.py

```

### Content Discovery
```
python3 fb_ads_optimization/charts.py # generate charts
python3 fb_ads_optimization/insights.py # get insights
```
