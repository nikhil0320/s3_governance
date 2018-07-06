import logging
import os
import botocore
from utils.common_utils import get_config, notify_email, get_aws_resource
from utils.logger_utils import LoggerUtils as logger


toEmail = os.environ['ToEmail']
fromEmail = os.environ['FromEmail']

#logger = logging.getLogger()
#logger.setLevel() = 'DEBUG'

def encryption_enabled(bucketName, s3, subscriberAccountId):
    """This function will return whether the Bucket is encrypted or not."""
    try:
        s3.get_bucket_encryption(Bucket=bucketName)
        logger.logInfo(f'S3 bucket: {bucketName} is already encrypted in Account number:{subscriberAccountId}')
        return True
    except botocore.exceptions.ClientError as error:
        if 'ServerSideEncryptionConfigurationNotFoundError' in str(error):
            return False
        else:
            logger.logError(Bucket f'{bucketName} in {subscriberAccountId} not encrypted due to following error: \n {error}')
            message = f'S3 Bucket {bucketName} in {subscriberAccountId} not encrypted due to following error: \n {error}'
            logger.logDebug(f'sent error email')
            notify_email(toEmail, fromEmail, message)
            return True


def enable_encryption(bucketName, s3, subscriberAccountId):
    """ This function enables the encryption on bucket """
    try:
        s3.put_bucket_encryption(Bucket=bucketName, ServerSideEncryptionConfiguration={'Rules':[{'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}},]})
        logger.logDebug(f'Encrypted successfully and sent mail')
        message = f'{bucketName} in account number: {subscriberAccountId} successfully encrypted.'
        notify_email(toEmail, fromEmail, message)
        return True
    except botocore.exceptions.ClientError as error:
        message =  f'Bucket {bucketName} in {subscriberAccountId} is not encrypted successfully due to following \n {error}'
        logger.logError(f'Bucket {bucketName} in {subscriberAccountId} is not encrypted successfully due to following \n {error}')
        notify_email(toEmail, fromEmail, message)


def lambda_handler(event, context):
    """This is main lambda function"""
    bucketName = event['detail']['requestParameters']['bucketName']
    subscriberAccountId = event['account']
    sessionName = context.function_name
    #sessionName = 's3_governance'
    cbcapMgmtRoleName = os.environ['mgmt_role_common_name']
    s3 = get_aws_resource('s3', subscriberAccountId, cbcapMgmtRoleName, sessionName)
    if not encryption_enabled(bucketName, s3, subscriberAccountId):
        encryption_status = enable_encryption(bucketName, s3, subscriberAccountId)
        if encryption_status:
            logger.logDebug(f'Lambda {sessionName} executed and {bucketName} in {subscriberAccountId} successfully encrypted')
        else:
            logger.logError(f'Lambda Execution Failed.')
