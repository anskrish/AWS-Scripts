import boto3

bucket_name = 'esx-test'
s3_file_path= 'unit/89324222322/test.csv'
save_as = 's3.csv'

s3 = boto3.client('s3')
s3.download_file(bucket_name , s3_file_path, save_as)
