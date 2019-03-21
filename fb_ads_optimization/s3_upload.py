import calendar
import os
import time

import boto3

s3_folder = 'ada-reports'
local_folder = './reports'

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Get all the png reports in the folder
files = [file for file in os.listdir(local_folder) if file.endswith('.png')]

# Upload the reports to S3
for f in files:
    file_name = str(f.split(".")[0] + "-{}.png").format(calendar.timegm(time.gmtime()))

    print("\nUploading file \"{}\" to s3 folder \"{}\"".format(file_name, s3_folder))

    data = open("{}/{}".format(local_folder, f), 'rb')
    s3.Bucket(s3_folder).put_object(Key=file_name, Body=data)
