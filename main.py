import json
import requests

TELEGRAM_TOKEN = ""
CHAT_ID = ""


def lambda_handler(event, context):
    print(event)

    message = "Webhook Received"
    send_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=HTML&text=' + message

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
