import os
import boto3

def lambda_handler(event, context):
    sesClient=boto3.client('ses')
    sub=os.environ['Email_Subject']
    vio=os.environ['Violation']
    remidate=os.environ['Remediation']
    raf=event['source']
    rid=event['id']
    region=event['region']
    name=event['detail']['requestParameters']['bucketName']
    arn=f'arn:aws:s3:::{name}'
    type=event['detail']['eventSource']
    ano=event['account']
    
    email = f'"subject":"{sub}" , "violation": "{vio}", "remediation": "{remidate}", "raffect": "{raf}", "rid": "{rid}", "rname": "{name}", "rtype": "{type}", "rarn": "{arn}", "rregion":"{region}", "accno":"{ano}"'

    
    sesClient.send_templated_email(
    Source='nikhil.linga@reancloud.com',
    Destination={
        'ToAddresses': [
            'nikhil.linga@reancloud.com',
        ]
    },
 
    Template='CBCAP_SES_TEMPLATE',
    TemplateData= '{'+email+'}'
   )
 
