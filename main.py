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

    return {
        'statusCode': 200,
        'body': json.dumps(log)
    }

def scrapy_request(body):
    body_stats = body.get("stats", {})

    template = "<pre>{}\n\n\n{}</pre>"

    stats_table = (
        "| Statistics Name                         | Statistics Value             \n"
        "| --------------------------------------- | -----------------------------\n"
    )

    for stats in body_stats.keys():
        stats_table = stats_table + "| {0:<40}| {1}".format(
            stats, body_stats[stats]
        ) + "\n"

    message = template.format(
        body["spider"].upper(),
        stats_table.upper()
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
