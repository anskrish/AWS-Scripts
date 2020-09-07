import boto3
import sys

# execution  : python sg-list.py  sg-name
ec2 = boto3.client('ec2') # for client interface


all_instances = ec2.describe_instances() 

#Filtering all SG's based on sys org.
all_sg = ec2.describe_security_groups(Filters=[dict(Name='group-name', Values=[sys.argv[1]])])


instance_sg_set = set()
sg_set = set()

for reservation in all_instances["Reservations"] :
  for instance in reservation["Instances"]: 
    for sg in instance["SecurityGroups"]:
      instance_sg_set.add(sg["GroupName"]) 

for security_group in all_sg["SecurityGroups"] :
  sg_set.add(security_group ["GroupName"])

idle_sg = sg_set - instance_sg_set

# Checking if any un-used SG's found
if len(idle_sg) == 0:
    print "Did not find any un-used SG with name", str(sys.argv[1])
else:
    for elem in idle_sg:
        response = ec2.describe_security_groups(Filters=[dict(Name='group-name', Values=[(elem)])])
        sg_id = response['SecurityGroups'][0]['GroupId']
        #Deleting Un-used SG's
#        ec2.delete_security_group(GroupId=sg_id)
        print "Deleted Unused SecurityGroups", elem, sg_id
