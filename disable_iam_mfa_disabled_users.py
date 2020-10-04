import boto3
import datetime
import botocore.exceptions

def disable_aws_user_console(client, username):
    print ('Processing for user:%s Disabling Console Access' %(username))
    try:
        response = client.delete_login_profile(UserName=username)
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'NoSuchEntity':
            print('Login Profile already disabled for User %s' %(username))
        else:
            print("Unexpected error: %s" % err)


def main():
    client = boto3.client('iam')
   # group = client.get_group(GroupName='users',)
    all_users = client.list_users()
    no_mfa_users = []
    for user in all_users['Users']:
        username = user['UserName']
        response = client.list_mfa_devices(UserName=username)
        if not response['MFADevices']:
            no_mfa_users.append(username)
    for username in no_mfa_users:
        disable_aws_user_console(client,username)
        
if __name__ == "__main__":
    main()
