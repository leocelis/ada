"""
Create ~/.aws/credentials with
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

"""
import calendar
import os
import time

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Get all the png reports in the folder
files = [file for file in os.listdir('.') if file.endswith('.png')]

# Upload the reports to S3
for f in files:
    data = open(f, 'rb')
    file_name = str(f.split(".")[0] + "-{}.png").format(calendar.timegm(time.gmtime()))
    print(file_name)
    s3.Bucket('ada-reports').put_object(Key=file_name, Body=data)
