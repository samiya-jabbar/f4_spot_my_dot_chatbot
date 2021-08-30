from dialogflow_fulfillment import QuickReplies, WebhookClient, Payload
from flask import Flask, request, Response, jsonify , make_response
import json
import requests

app = Flask(__name__)

#Handle the webhook request

def handler(agent: WebhookClient) :

    req = request.get_json(force=True)
    intent_name = req.get('queryResult').get('intent').get('displayName')
    url1= 'http://aiderma.ew.r.appspot.com/auth_account'
    url2 = 'http://aiderma.ew.r.appspot.com/fetch_metadata'
    url3 = 'http://aiderma.ew.r.appspot.com/store_and_diagnose_image'
    url4 = 'http://aiderma.ew.r.appspot.com/create_account'

#ferching name of a user during whole conversation

    def fetching_name():
        userid = agent.context.get('session-vars').get('parameters').get('userid')
        myobj = {'userid' : userid }
        x = requests.post(url2, data = myobj)
        x = x.text
        result = json.loads(x)
        name = result['metadata']['name']
        return name

#introduction of chatbot

    if intent_name == 'intro':
        agent.add('I am the chatbot of this page. Ready to assist you with anything you need. What would you like to do?')
        agent.add(QuickReplies(quick_replies=['START NOW','LOGIN']))

#Collecting all info during signup process 

    if intent_name == 'get_started_dontget_history_signedup' or intent_name == 'get_started_get_history_signedupp' or intent_name == 'get_started_get_history_signedup' or intent_name == 'get_started_dontget_history_signedupp' or intent_name == 'get_started_dontget_history_signeduppp' or intent_name =='get_started_get_history_signeduppp' or intent_name == 'get_started_get_history_signedupppp' or intent_name == 'get_started_dontget_history_signedupppp' :
        name = agent.context.get('session-vars').get('parameters').get('name')['name']
        print('name', name)
        userid = agent.context.get('session-vars').get('parameters').get('email')
        print('userid', userid)
        pwd = agent.context.get('session-vars').get('parameters').get('pwd')
        print('pwd', pwd)
        age = agent.context.get('session-vars').get('parameters').get('age')
        print('age', age)
        image = agent.context.get('session-vars').get('parameters').get('image')
        print('image', image)
        history = req.get('queryResult').get("queryText")
        print('history', history)      
        myobj = {'userid': userid, 'pwd': pwd, 'name' : name,  'age' : age,  'image' : image,  'history' : history}
        x = requests.post(url4, data = myobj)
        print(x)
        x = x.text
        result = json.loads(x)
        print(result)
        if result['status']== 'OK':
            agent.set_followup_event("account_created_now_login")
        else:       
            agent.set_followup_event("awaiting_for_again_signup")

    if intent_name == 'get_started_signup':
        agent.set_followup_event("awaiting_click_on_startnow_button")

#successfully created an account now chatbot is asking user to login here 

    if intent_name == 'account_created_now_login':
        agent.add('You have successfully created your account at SPOT MY DOT')
        agent.add(QuickReplies(quick_replies=['LOGIN NOW', 'GO BACK']))

#If account not created (due to incomplete info/ wrong info) chatbot is giving a chance to signup again

    if intent_name == 'again_signup':
        agent.add('There is an error while creating your account, Please try Again!')
        agent.add(QuickReplies(quick_replies=['SIGNUP HERE']))

#Login process

    if intent_name == 'login':
        agent.set_followup_event("awaiting_click_on_logon_button")

    if intent_name == 'login_screen' :  
        userid = req.get('queryResult').get('parameters').get('userid')
        pwd = req.get('queryResult').get('parameters').get('pwd')
        myobj = {'userid': userid, 'pwd': pwd }
        x = requests.post(url1, data = myobj)
        x = x.text
        result = json.loads(x)
        print(type(result))
        print(result)
        print(result['status'])
        if result['status'] == "OK":
            name = fetching_name()
            agent.add(f'Hi {name}. I’m your personal dermatologist! Need my help to diagnose your skin moles or birthmarks…?')
            agent.add(QuickReplies(quick_replies=['TAKE A PICTURE','BACK TO PROFILE']))
            choice = req.get('queryResult').get('queryText')
            if choice == 'TAKE A PICTURE':
                print("ok")
                agent.set_followup_event("start_chatbot")
            if choice == 'BACK TO PROFILE':
                agent.set_followup_event("back_to_profile")
        else:
            agent.set_followup_event("awaiting_for_again_login")

#While login (due to incomplete info/ wrong info) chatbot is giving a chance to login again

    if intent_name == 'again_login':
        agent.add('You have provided incorrect credentials, Please Try Again!')
        agent.add(QuickReplies(quick_replies=['LOGIN HERE', 'GO BACK']))

#After successfully login chatbot is asking to capture a picture of mole

    if intent_name == 'take_a_pic':
        name = fetching_name()
        agent.add(f'Ok,{name}! Let’s get started… I just need you to upload an image or take a picture so I can see what your suspicious mole, birthmark, or skin lesion looks like. Thanks!')
        agent.add(QuickReplies(quick_replies=['CAMERA', 'UPLOAD']))

    if intent_name == 'camera_mode':
        name = fetching_name()
        agent.add(f'{name}, please go ahead and hold the camera over the suspicious mole (from around 10-15cmaway). Move around until the red circle turns green – this means your skin lesion is in focus and you can take a photo. Thanks!')
        agent.add(QuickReplies(quick_replies=['UPLOAD']))

#After succesfully captured a picture a chatbot is asking to upload this picture for analysis

    if intent_name == 'upload_a_captured_image':
        userid = req.get('queryResult').get('parameters').get('userid')
        name = fetching_name()
        image = req.get('queryResult').get('parameters').get('image')
        myobj = {'userid' : userid,'image': image }
        x = requests.post(url3, data = myobj)
        result = x.text
        print(result) 
        agent.add(f'Thanks for that, {name}! Your picture looks great! I can see the skin lesion clearly. Please give me a few moments to analyze your photo and provide a diagnosis ASAP')
        #diagnose_output = x['diagnose_output']
        #time_stamp = x['time_stamp']
        # For green = 1 , yellow = 2 , red = 3 , unknown = 0
        diagnose_output = 1
        if diagnose_output == 1:
            agent.set_followup_event('result_is_green')
        if diagnose_output == 2:
            agent.set_followup_event('result_is_yellow')
        if diagnose_output == 3:
             agent.set_followup_event('result_is_red')
        if diagnose_output == 0:
             agent.set_followup_event('result_is_unknown')

#Response of chatbot on different colours 
# 1.green 
# 2.yellow
# 3.red

    if intent_name == 'result_green':
        agent.add('Good news! Looks like you’ve got a non-cancerous skin lesion. Are there any other moles you want me to take a look at?(yes/no)')

    if intent_name == 'result_green - no':
        name = fetching_name()
        agent.add(f'Have a great day {name}, and thanks for using SpotMyDot!')

    if intent_name == 'result_green - yes':
        agent.add('Ok, let me take another look')
        agent.add(QuickReplies(quick_replies=['CAMERA', 'UPLOAD']))

    if intent_name == 'result_yellow':
        name = fetching_name()
        print(name)
        agent.add(f'{name}, I’ve detected a pre-cancerous skin lesion that has the potential to develop into cancer if left untreated. Don’t panic – the next step would be to book an appointment with a dermatologist for a second opinion. Would you like me to make the booking for you?(yes/no)')

    if intent_name == 'result_yellow - no':
        name = fetching_name()
        agent.add(f'Ok {name}, have a great day further.')

    if intent_name == 'result_yellow - yes':
        agent.add('Let’s book your appointment / want to take another picture?')
        agent.add(QuickReplies(quick_replies=['BOOK A DERMATOLOGIST', 'CAMERA', 'UPLOAD']))

    if intent_name == 'result_red':
        name = fetching_name()
        agent.add(f'{name}, it seems you have a cancerous skin lesion. I strongly recommend you book a personal appointment with a dermatologist as soon as possible – I can help you book it now if you want. Would you like me to go ahead and make the booking?(yes/no)')

    if intent_name == 'result_red - no':
        name = fetching_name()
        agent.add(f'Ok {name}, have a great day further.')

    if intent_name == 'result_red - yes':
        agent.add('Ok, let’s secure your appointment.')
        agent.add(QuickReplies(quick_replies=['BOOK A DERMATOLOGIST']))

    if intent_name == 'result_unknown':
        name = fetching_name()
        agent.add(f'{name}, I’m struggling to provide a diagnosis for this skin lesion – the best thing to do would be to book an in-person appointment with a dermatologist. Best of luck, and have a great day further!')
        agent.add(QuickReplies(quick_replies=['BOOK A DERMATOLOGIST', 'GO BACK']))

#Back to profile if not interested to capture picture of mole

    if intent_name == 'back_to_profile':  
        userid = agent.context.get('session-vars').get('parameters').get('userid') 
        pwd = agent.context.get('session-vars').get('parameters').get('pwd') 
        myobj = {'userid': userid, 'pwd': pwd }
        x = requests.post(url1, data = myobj)
        x = x.text
        result = json.loads(x)
        if result['status'] == "OK":
            name = fetching_name()
            agent.add(f'Hi {name}. This is your DASHBOARD and I’m your personal dermatologist! Need my help to diagnose your skin moles or birthmarks…?')
            agent.add(QuickReplies(quick_replies=['TAKE A PICTURE']))
            choice = req.get('queryResult').get('queryText')
            if choice == 'TAKE A PICTURE':
                print("ok")
                agent.set_followup_event("start_chatbot")
        else:
            agent.set_followup_event("awaiting_for_again_login")

#schedule an appointment once got a response(result) from chatbot

    if intent_name == 'appointment_screen':
        url='http://aiderma.ew.r.appspot.com/book_an_appointment'
        agent.add('Appointment Booked ! NEED TO RESCHEDULE?')
        agent.add(QuickReplies(quick_replies=['Yes', 'No']))

#reschedule an appointment

    if intent_name == 'reschedule_appointment - yes':
        agent.add('OK, Reschedule your appointment Please')
        agent.add(QuickReplies(quick_replies=['BOOK A DERMATOLOGIST']))

    if intent_name == 'reschedule_appointment - no':
        agent.add('OK, Thanks for using SpotMyDot! Take Care!')


#Handle webhook requests from Dialogflow.

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    agent = WebhookClient(req)
    agent.handle_request(handler)
    return agent.response

if __name__ == '__main__':
    app.run(debug=True)

