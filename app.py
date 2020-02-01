from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages?EAALDLMirOvEBANQZB3QtTFMlmxwuOi6XYvO06tqDgkl72xbjQptFgVoHHGWR5etfHc6ow7DwkmBrq2vNTnZCCeuWXusa852lOTc8iZAeVZAiRIZAxXgui2xouUvNV1mhClQbvG98AKrrQBZATO5tsEaeZCsKeAj5Jdot1G2DbU7ajwCr8dCPaEq'
VERIFY_TOKEN = 'hafeezkhan1806'
PAGE_ACCESS_TOKEN = 'EAALDLMirOvEBANQZB3QtTFMlmxwuOi6XYvO06tqDgkl72xbjQptFgVoHHGWR5etfHc6ow7DwkmBrq2vNTnZCCeuWXusa852lOTc8iZAeVZAiRIZAxXgui2xouUvNV1mhClQbvG98AKrrQBZATO5tsEaeZCsKeAj5Jdot1G2DbU7ajwCr8dCPaEq'


def get_bot_response(message):
 input = message
 with open("data.json", "r") as jsonFile: #open file
  data = json.load(jsonFile)
  ret = data[input]  
 return(ret) 
   
 


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))
			


def send_message(recipient_id, text):
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()			


@app.route("/",methods=['GET','POST'])
def listen():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)
        return "ok"
		
if __name__ == "__main__":
 app.run()		
