import boto3
import datetime
import botocore.exceptions
client = boto3.client('iam')
group = client.get_group(GroupName='users',)

for user in group['Users']:
    username = user['UserName']
    if 'PasswordLastUsed' in user:
        lastpassword_used_date = user['PasswordLastUsed']
        lastpassword_used_required_format_date = lastpassword_used_date.date()
        todaydate = datetime.date.today()
        user_inactive_days = (todaydate - lastpassword_used_required_format_date).days
    else:
        user_inactive_days = "NA"
    if user_inactive_days > 90 :
        try:
            check_console_access_status = client.get_login_profile(UserName=(username))
            user_creation_date=user['CreateDate']
            user_creation_required_format_date = user_creation_date.date()
            user_creation_days = (todaydate - user_creation_required_format_date).days
            if user_creation_days > 90 :
                print '%(username)s %(user_inactive_days)s' % globals()
            
        except botocore.exceptions.ClientError as err:
            output = "User profile already disabled"
            #print '%(username)s %(output)s' % globals()
    