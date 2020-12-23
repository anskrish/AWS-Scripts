import boto3
import csv
import datetime
client = boto3.client('ec2')
file_name = 'aws_all_resources.csv'
count=1
csv_ob=open(file_name,"a")
csv_w=csv.writer(csv_ob)

redis_client = boto3.client('elasticache')
redis_response = redis_client.describe_cache_clusters()
redis_subnetlist=[]
for subnetgroup in redis_response['CacheClusters']:
    redis_subnetlist.append(subnetgroup['CacheSubnetGroupName'])
redis_subnet_group_without_dublicate_list = list(set(redis_subnetlist))


csv_w.writerow(["S.No","VPC-Id","VPC-CIDR","VPC-Name-Tag","Subnet","Subnet-CIDR","Subnet-Tag-Name","Availability-Zone","Instance-id","Instance-Private-Ip","Instance-Name-Tag","RDS-Instance-Name","ELB-Name","ELB-Security-Group","Redis-Cluster-Name","NAT-Gateway","NAT-Gateway-Name-Tag"])
response = client.describe_vpcs()


for vpc in response['Vpcs']:
    vpc_tags=[]
    if 'Tags' in vpc:
        for vpctags in vpc['Tags']:
            vpc_tags.append(vpctags.get('Key'))
            if vpctags.get('Key') == "Name":
                subnet_client = client.describe_subnets(Filters=[{ 'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
                if not subnet_client['Subnets']:
                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),"No Subnets","","","","","","","","","","","",""])
                    count+=1
                else:
                    for subnet in subnet_client['Subnets']:
                        subnet_tags=[]
                        if 'Tags' in subnet:
                            for subnettags in subnet['Tags']:
                                subnet_tags.append(subnettags.get('Key'))
                                if subnettags.get('Key') == "Name":
                                    instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                                    if instance_response['Reservations']:
                                        for instance in instance_response['Reservations']:
                                            for instanceid in instance['Instances']:
                                                instance_tags=[]
                                                if 'Tags' in instanceid:
                                                    for instancetags in instanceid['Tags']:
                                                        instance_tags.append(instancetags.get('Key'))
                                                        if instancetags.get('Key') == "Name":
                                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                                            count+=1
                                                else:
                                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                                    count+=1
                                                if 'Tags' in instanceid and 'Name' not in instance_tags :
                                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                                    count+=1
                                    else:
                                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),"","","","","","","","",""])
                                        count+=1
                        else:
                            instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                            if instance_response['Reservations']:
                                for instance in instance_response['Reservations']:
                                    for instanceid in instance['Instances']:
                                        instance_tags=[]
                                        if 'Tags' in instanceid:
                                            for instancetags in instanceid['Tags']:
                                                instance_tags.append(instancetags.get('Key'))
                                                if instancetags.get('Key') == "Name":
                                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                                    count+=1
                                        else:
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                                        if 'Tags' in instanceid and 'Name' not in instance_tags :
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                            else:
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","","",""])
                                count+=1
                        if 'Tags' in subnet and 'Name' not in subnet_tags:
                            instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                            if instance_response['Reservations']:
                                for instance in instance_response['Reservations']:
                                    for instanceid in instance['Instances']:
                                        instance_tags=[]
                                        if 'Tags' in instanceid:
                                            for instancetags in instanceid['Tags']:
                                                instance_tags.append(instancetags.get('Key'))
                                                if instancetags.get('Key') == "Name":
                                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                                    count+=1
                                        else:
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                                        if 'Tags' in instanceid and 'Name' not in instance_tags :
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                            else:
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","","",""])
                                count+=1
                        rds_client = boto3.client('rds')
                        rds_response = rds_client.describe_db_instances()
                        for rds in rds_response['DBInstances']:
                            for rdssubnet in rds['DBSubnetGroup']['Subnets']:
                                if rdssubnet.get('SubnetIdentifier') == subnet['SubnetId']:
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","",(rds['DBInstanceIdentifier']),"","","","",""])
                                    count+=1
                        elb_client = boto3.client('elb')
                        lbs = elb_client.describe_load_balancers()
                        for elb in lbs['LoadBalancerDescriptions']:
                            for elb_subnet in elb['Subnets']:
                                if elb_subnet == subnet['SubnetId']:
                                    groupname=elb['SecurityGroups']
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","",elb['LoadBalancerName'],(groupname),"","",""])
                                    count+=1
                        for i in redis_subnet_group_without_dublicate_list:
                            redis_subnet_ids=[]
                            response_redis_subnet_group = redis_client.describe_cache_subnet_groups(CacheSubnetGroupName=i)
                            for redis_subnet_group in response_redis_subnet_group['CacheSubnetGroups']:
                                for subnetid in redis_subnet_group['Subnets']:
                                    redis_subnet_ids.append(subnetid['SubnetIdentifier'])
                                if subnet['SubnetId'] in redis_subnet_ids:
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","",i,"",""])
                                    count+=1
                        natgateway_response = client.describe_nat_gateways(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']]}])
                        for natgateway in natgateway_response ['NatGateways']:
                            natgateway_tags=[]
                            if 'Tags' in natgateway:
                                for natgatewaytags in natgateway['Tags']:
                                    natgateway_tags.append(natgatewaytags.get('Key'))
                                    if natgatewaytags.get('Key') == "Name":
                                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],natgatewaytags.get('Value')])
                                        count+=1
                            else:
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],""])
                                count+=1
                            if 'Tags' in i and 'Name' not in natgateway_tags:
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],""])
                                count+=1

    else:
        subnet_client = client.describe_subnets(Filters=[{ 'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
        if not subnet_client['Subnets']:
            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"","No Subnets","","","","","","","","","","","",""])
            count+=1
        else:
            for subnet in subnet_client['Subnets']:
                subnet_tags=[]
                if 'Tags' in subnet:
                    for subnettags in subnet['Tags']:
                        subnet_tags.append(vpctags.get('Key'))
                        if subnettags.get('Key') == "Name":
                            instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                            if instance_response['Reservations']:
                                for instance in instance_response['Reservations']:
                                    for instanceid in instance['Instances']:
                                        instance_tags=[]
                                        if 'Tags' in instanceid:
                                            for instancetags in instanceid['Tags']:
                                                instance_tags.append(instancetags.get('Key'))
                                                if instancetags.get('Key') == "Name":
                                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                                    count+=1
                                        else:
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                                        if 'Tags' in instanceid and 'Name' not in instance_tags :
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                        else:
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),"","","","","","","","",""])
                            count+=1   
                else:
                    instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                    if instance_response['Reservations']:
                        for instance in instance_response['Reservations']:
                            for instanceid in instance['Instances']:
                                instance_tags=[]
                                if 'Tags' in instanceid:
                                    for instancetags in instanceid['Tags']:
                                        instance_tags.append(instancetags.get('Key'))
                                        if instancetags.get('Key') == "Name":
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                            count+=1
                                else:
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                                if 'Tags' in instanceid and 'Name' not in instance_tags :
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                    else:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","","",""])
                        count+=1
                if 'Tags' in subnet and 'Name' not in subnet_tags:
                    instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                    if instance_response['Reservations']:
                        for instance in instance_response['Reservations']:
                            for instanceid in instance['Instances']:
                                instance_tags=[]
                                if 'Tags' in instanceid:
                                    for instancetags in instanceid['Tags']:
                                        instance_tags.append(instancetags.get('Key'))
                                        if instancetags.get('Key') == "Name":
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                            count+=1
                                else:
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                                if 'Tags' in instanceid and 'Name' not in instance_tags :
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                    else:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","","",""])
                        count+=1
                rds_client = boto3.client('rds')
                rds_response = rds_client.describe_db_instances()
                for rds in rds_response['DBInstances']:
                    for rdssubnet in rds['DBSubnetGroup']['Subnets']:
                        if rdssubnet.get('SubnetIdentifier') == subnet['SubnetId']:
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","",(rds['DBInstanceIdentifier']),"","","","",""])
                            count+=1
                elb_client = boto3.client('elb')
                lbs = elb_client.describe_load_balancers()
                for elb in lbs['LoadBalancerDescriptions']:
                    for elb_subnet in elb['Subnets']:
                        if elb_subnet == subnet['SubnetId']:
                            groupname=elb['SecurityGroups']
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","",elb['LoadBalancerName'],(groupname),"","",""])
                            count+=1
                for i in redis_subnet_group_without_dublicate_list:
                    redis_subnet_ids=[]
                    response_redis_subnet_group = redis_client.describe_cache_subnet_groups(CacheSubnetGroupName=i)
                    for redis_subnet_group in response_redis_subnet_group['CacheSubnetGroups']:
                        for subnetid in redis_subnet_group['Subnets']:
                            redis_subnet_ids.append(subnetid['SubnetIdentifier'])
                        if subnet['SubnetId'] in redis_subnet_ids:
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","",i,"",""])
                            count+=1
                natgateway_response = client.describe_nat_gateways(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']]}])
                for natgateway in natgateway_response ['NatGateways']:
                    natgateway_tags=[]
                    if 'Tags' in natgateway:
                        for natgatewaytags in natgateway['Tags']:
                            natgateway_tags.append(natgatewaytags.get('Key'))
                            if natgatewaytags.get('Key') == "Name":
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],natgatewaytags.get('Value')])
                                count+=1
                    else:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],""])
                        count+=1
                    if 'Tags' in i and 'Name' not in natgateway_tags:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],""])
                        count+=1
    if 'Tags' in vpc and 'Name' not in vpc_tags: 
        subnet_client = client.describe_subnets(Filters=[{ 'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
        if not subnet_client['Subnets']:
            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"","No Subnets","","","","","","","","","",""])
            count+=1
        else:
            for subnet in subnet_client['Subnets']:
                subnet_tags=[]
                if 'Tags' in subnet:
                    for subnettags in subnet['Tags']:
                        subnet_tags.append(vpctags.get('Key'))
                        if subnettags.get('Key') == "Name":
                            instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                            if instance_response['Reservations']:
                                for instance in instance_response['Reservations']:
                                    for instanceid in instance['Instances']:
                                        instance_tags=[]
                                        if 'Tags' in instanceid:
                                            for instancetags in instanceid['Tags']:
                                                instance_tags.append(instancetags.get('Key'))
                                                if instancetags.get('Key') == "Name":
                                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                                    count+=1
                                        else:
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                                        if 'Tags' in instanceid and 'Name' not in instance_tags :
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                            count+=1
                            else:
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),(subnettags.get('Value')),(subnet['AvailabilityZone']),"","","","","","","","",""])
                                count+=1
                else:
                    instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']] }])
                    if instance_response['Reservations']:
                        for instance in instance_response['Reservations']:
                            for instanceid in instance['Instances']:
                                instance_tags=[]
                                if 'Tags' in instanceid:
                                    for instancetags in instanceid['Tags']:
                                        instance_tags.append(instancetags.get('Key'))
                                        if instancetags.get('Key') == "Name":
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                            count+=1
                                else:
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                                if 'Tags' in instanceid and 'Name' not in instance_tags :
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                    else:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","","",""])
                        count+=1
                if 'Tags' in subnet and 'Name' not in subnet_tags:
                    instance_response = client.describe_instances(Filters=[{ 'Name': 'subnet-id', 'Values': [ subnet['SubnetId'] ] }])
                    if instance_response['Reservations']:
                        for instance in instance_response['Reservations']:
                            for instanceid in instance['Instances']:
                                instance_tags=[]
                                if 'Tags' in instanceid:
                                    for instancetags in instanceid['Tags']:
                                        instance_tags.append(instancetags.get('Key'))
                                        if instancetags.get('Key') == "Name":
                                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),(instancetags.get('Value')),"","","","","",""])
                                            count+=1
                                else:
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                                if 'Tags' in instanceid and 'Name' not in instance_tags :
                                    csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),(instanceid['InstanceId']),(instanceid['PrivateIpAddress']),"","","","","","",""])
                                    count+=1
                    else:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),"",(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","","",""])
                        count+=1
                rds_client = boto3.client('rds')
                rds_response = rds_client.describe_db_instances()
                for rds in rds_response['DBInstances']:
                    for rdssubnet in rds['DBSubnetGroup']['Subnets']:
                        if rdssubnet.get('SubnetIdentifier') == subnet['SubnetId']:
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","",(rds['DBInstanceIdentifier']),"","","","",""])
                            count+=1
                elb_client = boto3.client('elb')
                lbs = elb_client.describe_load_balancers()
                for elb in lbs['LoadBalancerDescriptions']:
                    for elb_subnet in elb['Subnets']:
                        if elb_subnet == subnet['SubnetId']:
                            groupname=elb['SecurityGroups']
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","",elb['LoadBalancerName'],(groupname),"","",""])
                            count+=1
                for i in redis_subnet_group_without_dublicate_list:
                    redis_subnet_ids=[]
                    response_redis_subnet_group = redis_client.describe_cache_subnet_groups(CacheSubnetGroupName=i)
                    for redis_subnet_group in response_redis_subnet_group['CacheSubnetGroups']:
                        for subnetid in redis_subnet_group['Subnets']:
                            redis_subnet_ids.append(subnetid['SubnetIdentifier'])
                        if subnet['SubnetId'] in redis_subnet_ids:
                            csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","",i,"",""])
                            count+=1
                natgateway_response = client.describe_nat_gateways(Filters=[{ 'Name': 'subnet-id', 'Values': [subnet['SubnetId']]}])
                for natgateway in natgateway_response ['NatGateways']:
                    natgateway_tags=[]
                    if 'Tags' in natgateway:
                        for natgatewaytags in natgateway['Tags']:
                            natgateway_tags.append(natgatewaytags.get('Key'))
                            if natgatewaytags.get('Key') == "Name":
                                csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],natgatewaytags.get('Value')])
                                count+=1
                    else:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],""])
                        count+=1
                    if 'Tags' in i and 'Name' not in natgateway_tags:
                        csv_w.writerow([count,(vpc['VpcId']),(vpc['CidrBlock']),(vpctags.get('Value')),(subnet['SubnetId']),(subnet['CidrBlock']),"",(subnet['AvailabilityZone']),"","","","","","","",natgateway['NatGatewayId'],""])
                        count+=1
csv_ob.close()
