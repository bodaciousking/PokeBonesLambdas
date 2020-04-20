import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Assign4Players')

    if 'body' in event and event['body']:
        request_text = event['body']
        body = json.loads(request_text)
        if 'username' in body and 'score' in body:
            if not body['username']:
                return error_object('Bad request - username cannot be blank')
            if not body['score']:
                return error_object('Bad request - score cannot be blank')
            user_id = body['username']
            points = float(body['score'])
            player = table.get_item(
                Key={'user_id':user_id}
                )
            item = player['Item']
            real_score = float(item['playerSkill'])
            new_score =  real_score + points
            db_score = str(new_score)
            table.update_item(
                Key ={
                    'user_id':user_id
                },
                UpdateExpression = 'SET playerSkill = :playerSkill',
                ExpressionAttributeValues={
                    ':playerSkill': db_score,
                }
                )
           
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            return error_object('must send username and score')
    else:
        return error_object('Must have body on your request')        
def error_object(error_message):
    return {
        'statusCode': 200,
        'body': '{"error":"' + error_message + '"}' 
    }