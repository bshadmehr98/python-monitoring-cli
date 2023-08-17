import requests
import json


def send_slack_message(webhook_url, message):
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Message sent successfully to Slack!")
    else:
        print("Failed to send message to Slack. Status code:", response.status_code)
