from collections import defaultdict

import boto3
import csv

# execution  : python Ec2-Instance-Details.py

# Connect to EC2
ec2 = boto3.resource('ec2')

cnt=1

csv_ob=open("ec2-info.csv","w")
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_NO","Name",'Type','State','Private IP','Public IP','Launch Time'])
# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = defaultdict()
for instance in running_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
            csv_w.writerow([cnt,instance['name'],instance['instance.instance_type'],instance.state['Name'],'instance.private_ip_address','instance.public_ip_address','instance.launch_time'])
            cnt+=1

csv_ob.close()

