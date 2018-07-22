import boto3

sesClient = boto3.client('ses')
sesClient.create_template(
    Template={
        'TemplateName': 'CBCAP_SES_TEMPLATE',
        'SubjectPart': '{{subject}}',
        'HtmlPart': '<h3>CBCAP Cloud Environment Notification</h3> <p><br />This is to notify you about the violation of a rule configured in CBCAP cloud environment. </p> <ul> <li><b>Violation: </b> {{violation}}</li> <li><b>Action taken: </b>{{remediation}}</li> </ul> <p><br/>AWS resource details: </p> <ul> <li><b>Resource ID: </b>{{rid}}</li> <li><b>Resource Name: </b>{{rname}}</li> <li><b>Resource Type: </b>{{rtype}}</li> <li><b>Resource ARN: </b>{{rarn}}</li> <li><b>Resource Region: </b>{{rregion}}</li> <li><b>Resource Account: </b>{{accno}}</li> </ul> <p><br /><br /><b>IMPORTANT:</b> Please do not reply to this message or email address. <br /><br />Best Regards, <br />CBCAP Cloud Team</p>'
   })
