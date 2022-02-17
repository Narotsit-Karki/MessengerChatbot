""" A Simple Messenger Chat Bot"""
from flask import Flask, request, escape
from pymessenger import Bot
from nltk.chat.util import Chat, reflections
from nltk.chat.eliza import pairs 


app = Flask(__name__)
ACCESS_TOKEN = 'Token provided by facebook'
VERIFY_TOKEN = 'your private token'
bot = Bot(ACCESS_TOKEN)


@app.route("/chatbot", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        if request.args.get("hub.mode")  == 'subscribe':
             token = request.args.get("hub.verify_token")
             return verify_the_token(escape(token))
    else:
        output = request.get_json()
        entry_got = output['entry']
        for info in entry_got[0]['messaging']:
            recipient_id = info['sender']['id']
            try:
                if info['message'].get('text'):
                    msg = info['message']['text']
                    chat = Chat(pairs, reflections)
                    message_send = chat.converse(msg)
                    send_message(recipient_id, message_send)
                
                if info['message'].get('attachments'):
                    message_send = get_non_text_message()
                    send_message(recipient_id,message_send)

            except KeyError:
                pass

    return "Message Processed"


def verify_the_token(token):
    if token == VERIFY_TOKEN:
        response = request.args.get("hub.challenge")
        return response
    else: 
        return "Invalid token"



def get_non_text_message():
    sample_responses_1 = ["Superb picture!!", "Looking Beautiful :)", "Great effort!", "Looking Good!!"]
    return random.choice(sample_responses_1)


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == '__main__':
    app.run()
