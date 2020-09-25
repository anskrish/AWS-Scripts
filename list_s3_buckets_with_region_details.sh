#!/bin/bash
aws s3 ls | awk -F " " '{print $3}' > /tmp/buckets
while read data
do
	region=$(aws s3api get-bucket-location --bucket $data | jq '.LocationConstraint')
	if [ $region != "null" ];then
		echo $data $region
	else
		echo $data '"us-east-1"'
	fi
done< /tmp/buckets
