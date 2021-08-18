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

    if intent_name == 'login':
        agent.set_followup_event("awaiting_click_on_logon_button")


    if intent_name == 'login_screen' :
        global userid
        global pwd
        url = 'http://aiderma.ew.r.appspot.com/auth_account'
        userid = req.get('queryResult').get('parameters').get('email')
        print(userid)
        pwd = req.get('queryResult').get('parameters').get('pwd')
        print(pwd)
        myobj = {'userid': userid, 'pwd': pwd }
        x = requests.post(url, data = myobj)
        x = x.text
        result = json.loads(x)
        print(result)
        if result['status'] == "ok":
            agent.set_followup_event("start_chatbot")
        else:
            agent.add("Error while login")

    if intent_name == 'the_start':
        name = 'xyz'
        agent.add(f'Hi {name}. I’m your personaldermatologist! Need my help to diagnose your skin moles or birthmarks…?')
        agent.add(QuickReplies(quick_replies=['TAKE A PICTURE','BACK TO PROFILE']))

    if intent_name == 'back_to_profile':
        url = 'http://aiderma.ew.r.appspot.com/auth_account'
        myobj = {'userid' : userid,'pwd': pwd }
        x = requests.post(url, data = myobj)
        result = x.text
        print(result)
        agent.add(result) 

    if intent_name == 'take_a_pic':
        name = 'xyz'
        agent.add(f'Ok,{name}! Let’s get started…I just need you to press the camera button below so I can see what your suspicious mole, birthmark, or skin lesion looks like. Thanks!. #name.name, please go ahead and hold the camera over the suspicious mole (from around 10-15cm away). Move around until the red circle turns green – this means your skin lesion is in focus and you can take a photo. Thanks!')
        agent.add(QuickReplies(quick_replies=['CAMERA']))

    if intent_name == 'upload_a_captured_image':
        url = 'http://aiderma.ew.r.appspot.com/store_and_diagnose_image'
        image = req.get('queryResult').get('parameters').get('image')
        print(image)
        myobj = {'userid' : userid,'image': image }
        x = requests.post(url, data = myobj)
        result = x.text
        print(result) 

    if intent_name == 'signup':
        agent.set_followup_event("awaiting_click_on_startnow_button")

    if intent_name == 'again_signup':
        agent.add('Error creating account, Try Again')
        agent.add(QuickReplies(quick_replies=['SIGNUP HERE']))

    if intent_name == 'dont_get_bloodpressure signup_finally':
        name = req.get('queryResult').get('outputContexts')[1].get('parameters').get('name')
        print('name', name)
        userid = req.get('queryResult').get('outputContexts')[1].get('parameters').get('email')
        print('userid', userid)
        pwd = req.get('queryResult').get('outputContexts')[1].get('parameters').get('pwd')
        print('pwd', pwd)
        age = req.get('queryResult').get('outputContexts')[1].get('parameters').get('age')
        print('age', age)
        image = req.get('queryResult').get('outputContexts')[1].get('parameters').get('image')
        print('image', image)
        bloodpressure = req.get('queryResult').get("queryText")
        print('bloodpressure', bloodpressure)
        url = 'http://aiderma.ew.r.appspot.com/create_account'
        myobj = {'userid': userid, 'pwd': pwd, 'name' : name,  'age' : age,  'image' : image,  'bloodpressure' : bloodpressure}
        x = requests.post(url, data = myobj)
        x = x.text
        result = json.loads(x)
        if result['status']== 'ok':
            agent.set_followup_event("start_chatbot")
        else:       
            agent.set_followup_event("awaiting_for_again_signup")

    
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
        bloodpressure = req.get('queryResult').get('queryText')
        print('bloodpressure', bloodpressure)
        url = 'http://aiderma.ew.r.appspot.com/create_account'
        myobj = {'userid': userid, 'pwd': pwd, 'name' : name,  'age' : age,  'image' : image,  'bloodpressure' : bloodpressure}
        x = requests.post(url, data = myobj)
        x = x.text
        result = json.loads(x)
        if result['status']== 'ok':
            agent.set_followup_event("start_chatbot")
        else:       
            agent.set_followup_event("awaiting_for_again_signup")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Handle webhook requests from Dialogflow."""
    req = request.get_json(force=True)
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run(debug=True)

