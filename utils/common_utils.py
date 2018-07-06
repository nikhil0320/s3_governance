import boto3
import json
import os

def get_config(bucket, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    configuration = json.loads(obj.get()['Body'].read())
    return configuration


def get_aws_resource(resourceType, accountId, roleName, sessionName):
    """ This function Assumes role based on the resource"""
    stsClient = boto3.client('sts')
    role = stsClient.assume_role(RoleArn=f'arn:aws:iam::{accountId}:role/{roleName}', RoleSessionName=sessionName)
    accessKey = role['Credentials']['AccessKeyId']
    secretKey = role['Credentials']['SecretAccessKey']
    sessionToken = role['Credentials']['SessionToken']
    return boto3.client(resourceType, aws_access_key_id=accessKey, aws_secret_access_key=secretKey,
                        aws_session_token=sessionToken)


def notify_email(toEmail, fromEmail, message):
    """This function sends notification"""
    sesClient = boto3.client('ses')
    sesClient.send_email(Source=fromEmail,
                         Destination={'ToAddresses': [toEmail]},
                         Message={'Subject': {'Data': os.environ['Email_Subject']},
                                  'Body': {'Text': {'Data': message}}})


