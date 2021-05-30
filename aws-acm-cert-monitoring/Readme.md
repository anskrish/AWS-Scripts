Steps to use

1. Install fresh ubuntu 18.04 machine
2. Install python3
apt-get install python3-pip

3. copy the script and requirement.txt file in one directory.

mkdir acm-script
cp acm-monitor.py ./acm-script
cp requirements.txt ./acm-script

4. Install aws cli and configure your target aws account credentials
pip3 install awscli
pip3 install boto3
pip3 install --upgrade awscli
aws configure


5.  Switch to script folder and set the env variables

cd acm-script
pip3 install -q -r requirements.txt --upgrade
export REGIONS=us-east-1
export THRESHOLDS=7,30,45,60

7 --> check and provide cert details which are expired exactly in 7 days from today
30 -- > check and provide cert details which are expired exactly in 30 days from today
45 --> check and provide cert details which are expired exactly in 45 days from today
60 --> check and provide cert details which are expired less than 60 days from today



Example execution:

I$ export THRESHOLDS=7,30,45,200
I$ export REGIONS=us-east-1
I$ python3 acm-monitor.py 
Inform: 987333333ewew/us-west-2/*.sandbox.public.aws.tesm.com expires in 175 days
Critical: 987333333/us-west-2/sandbox1.public.aws.testm.com expired by -86 days
Out of 4 , 1 of our certificates already expired.
Out of 4 , 1 of our certificates, about to expire within the given threshold.
:Documents 2$ 
