import os
from boto.s3.connection import S3Connection

try:
    s3 = S3Connection(os.environ['API_KEY'])
    print("Key available")
except:
    print("Key unavailable")
