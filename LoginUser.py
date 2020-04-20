import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Assign4Players')

    if 'body' in event and event['body']:
        request_text = event['body']
        body = json.loads(request_text)
        if 'password' in body and 'username' in body:
            if not body['username']:
                return error_object('Bad request - username cannot be blank')
            if not body ['password']:
                return error_object('Bad request - password cannot be blank')
            user_id = body['username']
            try_pwd = body['password']
            response = table.get_item(
                Key={'user_id': user_id }
            )
            item = response['Item']
            if try_pwd == item['password']:
                return {
                    'statusCode': 200,
                    'body': json.dumps(item)
                }
            else:
                return error_object('Password does not match.')
        else:
            return error_object('must send username and pawwsord')
    else:
        return error_object('Must have body on your request')        
def error_object(error_message):
    return {
        'statusCode': 200,
        'body': '{"error":"' + error_message + '"}' 
    }