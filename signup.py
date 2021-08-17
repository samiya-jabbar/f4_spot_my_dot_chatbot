from dialogflow_fulfillment import QuickReplies, WebhookClient, Payload
from flask import Flask, request, Response, jsonify , make_response
import json
import requests

app = Flask(__name__)

def handler(agent: WebhookClient) :
    """Handle the webhook request.."""

    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name == 'intro':
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['START NOW','LOGIN']))

    if intent_name == 'dont_get_bloodpressure signup_finally':
        name = req.get('queryResult').get('outputContexts')[0].get('parameters').get('name')
        print('name', name)
        userid = req.get('queryResult').get('outputContexts')[0].get('parameters').get('email')
        print('userid', userid)
        pwd = req.get('queryResult').get('outputContexts')[0].get('parameters').get('pwd')
        print('pwd', pwd)
        age = req.get('queryResult').get('outputContexts')[0].get('parameters').get('age')
        print('age', age)
        image = req.get('queryResult').get('outputContexts')[0].get('parameters').get('image')
        print('image', image)
        bloodpressure = req.get('queryResult').get('outputContexts')[0].get('parameters').get('bloodpressure')
        print('bloodpressure', bloodpressure)
        url = 'http://aiderma.ew.r.appspot.com/create_account'
        myobj = {'userid': userid, 'pwd': pwd, 'name' : name,  'age' : age,  'image' : image,  'bloodpressure' : bloodpressure}
        x = requests.post(url, data = myobj)
        result=x.text
        agent.add(result)
        agent.set_followup_event("start_chatbot")


    
    if intent_name == 'get_bloodpressure signup_finally':
        name = req.get('queryResult').get('outputContexts')[0].get('parameters').get('name')
        print('name', name)
        userid = req.get('queryResult').get('outputContexts')[0].get('parameters').get('email')
        print('userid', userid)
        pwd = req.get('queryResult').get('outputContexts')[0].get('parameters').get('pwd')
        print('pwd', pwd)
        age = req.get('queryResult').get('outputContexts')[0].get('parameters').get('age')
        print('age', age)
        image = req.get('queryResult').get('outputContexts')[0].get('parameters').get('image')
        print('image', image)
        bloodpressure = req.get('queryResult').get('outputContexts')[0].get('parameters').get('bloodpressure')
        print('bloodpressure', bloodpressure)
        url = 'http://aiderma.ew.r.appspot.com/create_account'
        myobj = {'userid': userid, 'pwd': pwd, 'name' : name,  'age' : age,  'image' : image,  'bloodpressure' : bloodpressure}
        x = requests.post(url, data = myobj)
        result=x.text
        agent.add(result)
        agent.set_followup_event("start_chatbot")

     
     


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    req = request.get_json(force=True)
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run(debug=True)

