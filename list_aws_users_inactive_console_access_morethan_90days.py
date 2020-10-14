import boto3
import datetime
import csv
import argparse
import botocore.exceptions

parser = argparse.ArgumentParser()
parser.add_argument('--inactiveDays', required=True)

args = parser.parse_args()
inactiveDays = int(args.inactiveDays)


###execution "python3 list_aws_users_inactive_console_access_morethan_90days.py --inactiveDays 90" ###

client = boto3.client('iam')
group = client.get_group(GroupName='users',)
file_name = 'aws_inactive_user.csv'
target_file = '%s_%s' % (datetime.date.today().strftime('%Y_%m_%d'), file_name)
count=1
csv_ob=open(target_file,"a")
csv_w=csv.writer(csv_ob)
csv_w.writerow(["S.No","Username","AWS Console inactive login(Days)"])
for user in group['Users']:
    username = user['UserName']
    if 'PasswordLastUsed' in user:
        lastpassword_used_date = user['PasswordLastUsed']
        lastpassword_used_required_format_date = lastpassword_used_date.date()
        todaydate = datetime.date.today()
        user_inactive_days = (todaydate - lastpassword_used_required_format_date).days
    else:
        user_inactive_days = "NA"
    if user_inactive_days > inactiveDays:
        try:
            check_console_access_status = client.get_login_profile(UserName=(username))
            user_creation_date = user['CreateDate']
            user_creation_required_format_date = user_creation_date.date()
            user_creation_days = (todaydate - user_creation_required_format_date).days
            if user_creation_days > inactiveDays:
                print ('%s %s' %(user_email,user_inactive_days))
                csv_w.writerow([count,(user_email),(user_inactive_days)])
                count+=1        
    
        except botocore.exceptions.ClientError as err:
            output = "User profile already disabled"
	   #print '%(username)s %(output)s' % globals() 
csv_ob.close()

