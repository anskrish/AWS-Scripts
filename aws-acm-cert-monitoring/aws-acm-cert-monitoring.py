import json
import logging
import os
from datetime import datetime

import boto3
import numpy as np
from botocore.exceptions import ClientError
from dateutil.parser import parse

sns_message_details = {

    'threshold0': {
        'Subject': 'Critical: {0}/{3}/{1} expired by {2} days',
        'Message': 'The SSL Certificate is already expired for Account #: {'
                   '0}, Region : {3}, Domain Name: {1}, Expiry Date: {2} '
    },
    'threshold1': {
        'Subject': 'High: {0}/{3}/{1} expires in {2} days',
        'Message': 'The SSL Certificate will expire for Account #: {0}, '
                   'Region : {4}, Domain Name: {1}, Expiry Date: {2}, '
                   'Remaining Days: {3} '
    },
    'threshold2': {
        'Subject': 'Medium: {0}/{3}/{1} expires in {2} days',
        'Message': 'The SSL Certificate will expire for Account #: {0}, '
                   'Region : {4}, Domain Name: {1}, Expiry Date: {2}, '
                   'Remaining Days: {3} '
    },
    'threshold3': {
        'Subject': 'Low: {0}/{3}/{1} expires in {2} days',
        'Message': 'The SSL Certificate will expire for Account #: {0}, '
                   'Region : {4}, Domain Name: {1}, Expiry Date: {2}, '
                   'Remaining Days: {3} '
    },
    'threshold4': {
        'Subject': 'Inform: {0}/{3}/{1} expires in {2} days',
        'Message': 'The SSL Certificate will expire for Account #: {0}, '
                   'Region : {4}, Domain Name: {1}, Expiry Date: {2}, '
                   'Remaining Days: {3} '
    }
}


regions = os.environ["REGIONS"].split(',')
thresholds = os.environ["THRESHOLDS"].split(",")
client = boto3.client('sts')
account_id = client.get_caller_identity()["Account"]
for region in regions:
    try:
        acm_client = boto3.client('acm', region)
        certificates = acm_client.list_certificates(CertificateStatuses=['ISSUED', 'EXPIRED'])
        certificates_count = np.array(certificates.get('CertificateSummaryList')).size
        acm_cert_list = []
        if certificates_count > 0:
            for item in certificates.get('CertificateSummaryList'):
                summary = subject = ""
                certificate_arn = item.get("CertificateArn")
                domain_name = item.get("DomainName")
                data = acm_client.describe_certificate(CertificateArn=certificate_arn)
                expiry_date = data.get("Certificate")["NotAfter"]

                parse_expiry_datetime = parse(str(expiry_date))
                now = datetime.utcnow()
                remaining_days = (parse(
                    parse_expiry_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")) - now).days
                # If remaining days is less than or equal to 0 days. It is considered
                # as already expired and need to be addressed as critical issue
                if int(remaining_days) <= 0:
                    subject = sns_message_details.get("threshold0").get("Subject").format(
                        account_id, domain_name, remaining_days, region)
                    summary = sns_message_details.get("threshold0").get("Message").format(
                        account_id, domain_name, expiry_date.strftime(
                            "%Y-%m-%d"), region)
                # If the number of remaining days is equal to first threshold value
                elif int(thresholds[0]) == int(remaining_days):
                    subject = sns_message_details.get("threshold1").get("Subject").format(
                        account_id, domain_name, remaining_days, region)
                    summary = sns_message_details.get("threshold1").get("Message").format(
                        account_id, domain_name, expiry_date.strftime(
                            "%Y-%m-%d"), remaining_days, region)
                # If the number of remaining days is equal to second threshold value
                elif int(thresholds[1]) == int(remaining_days):
                    subject = sns_message_details.get("threshold2").get("Subject").format(
                        account_id, domain_name, remaining_days, region)
                    summary = sns_message_details.get("threshold2").get("Message").format(
                        account_id, domain_name, expiry_date.strftime(
                            "%Y-%m-%d"), remaining_days, region)
                # If the number of remaining days is equal to third threshold value
                elif int(thresholds[2]) == int(remaining_days):
                    subject = sns_message_details.get("threshold3").get("Subject").format(
                        account_id, domain_name, remaining_days, region)
                    summary = sns_message_details.get("threshold3").get("Message").format(
                        account_id, domain_name, expiry_date.strftime(
                            "%Y-%m-%d"), remaining_days, region)
                # If the number of remaining days is equal to fourth threshold value
                elif int(thresholds[3]) >= int(remaining_days):
                    subject = sns_message_details.get("threshold4").get("Subject").format(
                        account_id, domain_name, remaining_days, region)
                    summary = sns_message_details.get("threshold4").get("Message").format(
                        account_id, domain_name, expiry_date.strftime(
                            "%Y-%m-%d"), remaining_days, region)

                if summary != "":
                    if subject is not None and len(subject) > 100:
                        raise ValueError(
                          'Subject must be less than 100 characters but current length of ( '
                          + subject + ' ) is '
                          + str(len(subject)))
                    print(subject)
          #          send_notification(region, sns_topic, subject, summary)
                    acm_cert_list.append([domain_name,remaining_days])
        if len(acm_cert_list) > 0:
          expired_count = sum(i[1] <= 0 for i in acm_cert_list)
          stand_by_count = sum(i[1] > 0 for i in acm_cert_list)
          if expired_count > 0:
            print("Out of " + str(certificates_count) + " , " + str(expired_count) + " of our certificates already expired.")
          if stand_by_count > 0:
            print("Out of " + str(certificates_count) + " , " + str(stand_by_count) + " of our certificates, about to expire within the given threshold.")
        else:
          print("No ACM certs are going to expire based on the given threshold.")
    except ClientError as e:
        logging.error(e)
