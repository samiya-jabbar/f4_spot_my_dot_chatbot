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

    if intent_name == 'ask_email':
        global name 
        name = req.get('queryResult').get('parameters').get('name')
        print(name)

    if intent_name == 'ask_pwd':
        global userid
        userid = req.get('queryResult').get('parameters').get('email')
        print(userid)

    if intent_name == 'ask_age':
        global pwd
        pwd = req.get('queryResult').get('parameters').get('pwd')
        print(pwd)

    if intent_name == 'ask_image':
        global age
        age = req.get('queryResult').get('parameters').get('age')
        print(age)

    if intent_name == 'ask_bp':
        global image
        image = req.get('queryResult').get('parameters').get('image')
        print(image)


    if intent_name == 'signed_up':
        bp = req.get('queryResult').get('parameters').get('bp')
        print(bp)
        url = 'http://aiderma.ew.r.appspot.com/create_account'
        print(userid)
        print(pwd)
        print(name)
        myobj = {'userid': userid, 'pwd': pwd , 'name' : name}
        x = requests.post(url, data = myobj)
        result=x.text
        agent.add(result)
        


    if intent_name == 'get_start':
        url = 'http://aiderma.ew.r.appspot.com/create_account'
        userid = req.get('queryResult').get('parameters').get('email')
        print(userid)
        pwd = req.get('queryResult').get('parameters').get('pwd')
        print(pwd)       
        name = req.get('queryResult').get('parameters').get('name')
        print(name)

    if intent_name == 'get_started - age':
        age = req.get('queryResult').get('parameters').get('age')['amount']
        print(age)

    if intent_name == 'get_started - image':
        image = req.get('queryResult').get('parameters').get('image')
        print(image)


        """ 
        if age == "none" :    
            myobj = {'userid': userid, 'pwd': pwd , 'name' : name}
            x = requests.post(url, data = myobj)
            result=x.text
            print("age not present")
            agent.add(result)

        if age != "none":
            myobj = {'userid': userid, 'pwd': pwd , 'name' : name, 'age' : age}
            x = requests.post(url, data = myobj)
            result=x.text
            print("age present")
            agent.add(result)

            """
            

    if intent_name == 'login_screen' :
        url = 'http://aiderma.ew.r.appspot.com/auth_account'
        userid = req.get('queryResult').get('parameters').get('email')
        print(userid)
        pwd = req.get('queryResult').get('parameters').get('pwd')
        print(pwd)
        myobj = {'userid': userid, 'pwd': pwd }
        x = requests.post(url, data = myobj)
        result = x.text
        print(result)
        agent.set_followup_event("start_chatbot")

    if intent_name == 'the_start':
        name = 'xyz'
        agent.add(f'Hi {name} .  I’m your personaldermatologist! Need my help to diagnose your skin moles or birthmarks…?')
        agent.add(QuickReplies(quick_replies=['TAKE A PICTURE','BACK TO PROFILE']))

    if intent_name == 'take_a_pic':
        name = 'xyz'
        agent.add(f'Ok,{name}! Let’s get started…I just need you to press the camera button below so I can see what your suspicious mole, birthmark, or skin lesion looks like. Thanks!. Do you want to upload that image?')
        agent.add(QuickReplies(quick_replies=['CAMERA']))

    if intent_name == 'camera_mode':
        agent.add(QuickReplies(quick_replies=['UPLOAD']))

    if intent_name == 'upload_a_captured_image':
        url = 'http://aiderma.ew.r.appspot.com/store_and_diagnose_image'
        image = req.get('queryResult').get('parameters').get('image')
        print(image)
        myobj = {'userid': userid, 'image': image }
        x = requests.post(url, data = myobj)
        result = x.text
        print(result)           

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

    imp = req.get('allRequiredParamsPresent')
        print(imp)
        if imp == 'true' :   
            myobj = {'userid': userid, 'pwd': pwd , 'name' : name}
            x = requests.post(url, data = myobj)
            print(x.text)
            agent.add("intent triggered")

         if (userid and pwd and name and age) == True:   
            myobj = {'userid': userid, 'pwd': pwd , 'name' : name , 'age' : age}

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
