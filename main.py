from dialogflow_fulfillment import QuickReplies, WebhookClient, Payload
from flask import Flask, request, Response, jsonify , make_response
import json
import requests

app = Flask(__name__)

def handler(agent: WebhookClient) :
    """Handle the webhook request.."""

    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name == 'Default Welcome Intent':
        agent.add('Alert! Losing gross margin due to decrease in price for 1 of your watched categories. I have identified a 9% decrease in price for  Nestlé Aero Dark Chocolate 400 gr x 6 SKU for the last 1 month in Chocolate category.')
        agent.add(QuickReplies(quick_replies=['High-level overview','In depth SKU analysis']))


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    req = request.get_json(force=True)
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run()
