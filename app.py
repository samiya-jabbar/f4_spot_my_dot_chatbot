from dialogflow_fulfillment import QuickReplies, WebhookClient, Payload
from flask import Flask, request, Response, jsonify , make_response
import json
import requests

app = Flask(__name__)

def handler(agent: WebhookClient) :
    """Handle the webhook request.."""
       
    url = 'http://aiderma.ew.r.appspot.com/auth_account'

    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name == 'intro':
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['START NOW','LOGIN']))

    if intent_name == 'get_started':
        userid = req.get('queryResult').get('parameters').get('email')
        print(userid)
        pwd = req.get('queryResult').get('parameters').get('pwd')
        print(pwd)
        name = req.get('queryResult').get('parameters').get('pwd')
        print(name)
        age = req.get('queryResult').get('parameters').get('pwd')
        print(age)
        myobj = {'userid': userid, 'pwd': pwd , 'name' : name}
        x = requests.post(url, data = myobj)
        print(x.text)
        agent.add("intent triggered")


    if intent_name == 'login_screen' :
        userid = req.get('queryResult').get('parameters').get('email')
        print(userid)
        pwd = req.get('queryResult').get('parameters').get('pwd')
        print(pwd)
        myobj = {'userid': userid, 'pwd': pwd }
        x = requests.post(url, data = myobj)
        print(x.text)

    if intent_name == 'name_number_1':
        name = req.get('queryResult').get('parameters').get('name')
        number = req.get('queryResult').get('parameters').get('phone-number') 
        user_concern = agent.context.get('awaiting_user_info').get('parameters').get('any')[0] 
 


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    req = request.get_json(force=True)
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run(debug=True)


"""

    if intent_name == 'get_started':
        agent.add('Ok, let’s create your account! Can I get the following from you?')
        agent.add('What is your full name?')

    if intent_name == 'get_started - age':
        agent.add('How old are you?')
       
    if intent_name== 'get_started - age - id_no':
        agent.add('What is your ID number?')
        
    if intent_name == 'get_started - age - id_no - password - optional_details':
        agent.add("Also, do you have any medical data available, like blood pressure or history of illness? It's is optional,but these will definitely help me build a better picture of you so that I can help as much as I can!")
     
    if intent_name == 'get_started - age - id_no - password - optional_details - save_data_to_firebase':
        name = req.get('queryResult').get('parameters').get('optional_details')
        print(name)
"""
