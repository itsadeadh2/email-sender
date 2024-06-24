def lambda_handler(event, context):
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": "I'm working!",
        "headers": {
            "content-type": "application/json"
        }
    }
