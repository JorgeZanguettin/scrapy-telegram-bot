import os
import json
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL_RESPONSE = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=HTML&text='

def lambda_handler(event, context):
    body = event_process(event)
    
    if "spider" in body:
        message, flag = scrapy_request(body)
    elif "message" in body:
        message, flag = telegram_request(body)
    else:
        raise Exception("Body resource not implemented")

    status_code = send_message(message)
    log = {
        "flag": flag,
        "message" : message,
        "status_code": status_code
    }
    print(log)

    return {
        'statusCode': 200,
        'body': json.dumps(log)
    }

def scrapy_request(body):
    body_stats = body.get("stats", {})

    template = "SPIDER: {}\nSTATS: {}"
    stats = ""

    for stat in body_stats.keys():
        stats += "{} - {}\n".format(
            stat, body_stats[stat]
        )

    message = template.format(
        body["spider"],
        stats
    )

    return message, "scrapy_request"

def telegram_request(body):
    return "", "telegram_request"

def send_message(message):
    message_url = URL_RESPONSE + message
    send = requests.get(message_url)

    return send.status_code

def event_process(event):
    body = event.get("body", {})
    if not body:
        raise Exception("Body is Empty")

    content = json.loads(body)
    stats = content.get("stats", {})

    if stats:
        content["stats"] = json.loads(stats)

    return content

lambda_handler(
    {'version': '1.0', 'resource': '/scrapy-telegram-bot', 'path': '/default/scrapy-telegram-bot', 'httpMethod': 'POST', 'headers': {'Content-Length': '818', 'Content-Type': 'application/json', 'Host': '9oo5ujc0c3.execute-api.us-east-1.amazonaws.com', 'User-Agent': 'python-requests/2.29.0', 'X-Amzn-Trace-Id': 'Root=1-651153e8-7e5ac58801648e7b0130e10a', 'X-Forwarded-For': '89.214.107.77', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br'}, 'multiValueHeaders': {'Content-Length': ['818'], 'Content-Type': ['application/json'], 'Host': ['9oo5ujc0c3.execute-api.us-east-1.amazonaws.com'], 'User-Agent': ['python-requests/2.29.0'], 'X-Amzn-Trace-Id': ['Root=1-651153e8-7e5ac58801648e7b0130e10a'], 'X-Forwarded-For': ['89.214.107.77'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https'], 'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'requestContext': {'accountId': '777450756162', 'apiId': '9oo5ujc0c3', 'domainName': '9oo5ujc0c3.execute-api.us-east-1.amazonaws.com', 'domainPrefix': '9oo5ujc0c3', 'extendedRequestId': 'LzoMXgYUoAMEYRw=', 'httpMethod': 'POST', 'identity': {'accessKey': None, 'accountId': None, 'caller': None, 'cognitoAmr': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityId': None, 'cognitoIdentityPoolId': None, 'principalOrgId': None, 'sourceIp': '89.214.107.77', 'user': None, 'userAgent': 'python-requests/2.29.0', 'userArn': None}, 'path': '/default/scrapy-telegram-bot', 'protocol': 'HTTP/1.1', 'requestId': 'LzoMXgYUoAMEYRw=', 'requestTime': '25/Sep/2023:09:33:28 +0000', 'requestTimeEpoch': 1695634408401, 'resourceId': 'ANY /scrapy-telegram-bot', 'resourcePath': '/scrapy-telegram-bot', 'stage': 'default'}, 'pathParameters': None, 'stageVariables': None, 'body': '{"spider": "datamaq", "stats": "{\\n    \\"downloader/request_bytes\\": 127712,\\n    \\"downloader/request_count\\": 171,\\n    \\"downloader/request_method_count/GET\\": 171,\\n    \\"downloader/response_bytes\\": 2762449,\\n    \\"downloader/response_count\\": 171,\\n    \\"downloader/response_status_count/200\\": 171,\\n    \\"elapsed_time_seconds\\": 17.86098,\\n    \\"finish_reason\\": \\"finished\\",\\n    \\"finish_time\\": \\"2023-09-25 09:33:27.753657\\",\\n    \\"item_scraped_count\\": 85,\\n    \\"memusage/max\\": 64311296,\\n    \\"memusage/startup\\": 64311296,\\n    \\"request_depth_max\\": 2,\\n    \\"response_received_count\\": 171,\\n    \\"scheduler/dequeued\\": 171,\\n    \\"scheduler/dequeued/memory\\": 171,\\n    \\"scheduler/enqueued\\": 171,\\n    \\"scheduler/enqueued/memory\\": 171,\\n    \\"start_time\\": \\"2023-09-25 09:33:09.892677\\"\\n}"}', 'isBase64Encoded': False},
    ""
)