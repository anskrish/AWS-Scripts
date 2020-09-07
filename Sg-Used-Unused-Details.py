import boto3
import sys
import csv

# execution  : python Sg-Used-Unused-Details.py
ec2 = boto3.client('ec2') # for client interface


all_instances = ec2.describe_instances() 


all_sg = ec2.describe_security_groups()

instance_sg_set = set()
sg_set = set()

cnt=1
csv_ob=open("sg-details.csv","w")
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S_NO","SG-ID","Used"])

for reservation in all_instances["Reservations"] :
  for instance in reservation["Instances"]: 
    for sg in instance["SecurityGroups"]:
      instance_sg_set.add(sg["GroupName"]) 

for security_group in all_sg["SecurityGroups"] :
  sg_set.add(security_group ["GroupName"])

for element in instance_sg_set:
  responsed = ec2.describe_security_groups(Filters=[dict(Name='group-name', Values=[(element)])])
  sg_id_instance = responsed['SecurityGroups'][0]['GroupId']
  csv_w.writerow([cnt,sg_id_instance,"yes"])
  cnt+=1



idle_sg = sg_set - instance_sg_set


# Checking if any un-used SG's found
if len(idle_sg) == 0:
    print "Did not find any un-used SG with name", str(sys.argv[1])
else:
    for elem in idle_sg:
        response = ec2.describe_security_groups(Filters=[dict(Name='group-name', Values=[(elem)])])
        sg_id = response['SecurityGroups'][0]['GroupId']
        csv_w.writerow([cnt,sg_id,"No"])
        cnt+=1
csv_ob.close()
        #Deleting Un-used SG's
#        ec2.delete_security_group(GroupId=sg_id)
