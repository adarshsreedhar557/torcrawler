from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()

slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))

def send_slack_notification(message):
    try:
        response = slack_client.chat_postMessage(channel=os.getenv("SLACK_CHANNEL"), text=message)
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
