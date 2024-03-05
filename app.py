from flask import Flask, render_template
from flask_socketio import SocketIO
import flask_sock
from flask_sock import Sock
from datetime import datetime
import time
import json
import string
from Comb import Comb

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('chad.html')
    

Messages = ""

comb_instance = Comb()

def add_msg(message,id):
    global Messages

    userMessage = """<div class="relative ml-64 mr-3 rounded-xl bg-white px-4 py-2 text-sm shadow">
                    <div class="mt-2 text-sm font-semibold">Du</div>
                    <div>%s</div>
                    </div>
                """
    llmMessage = """<div class="relative ml-3 mr-64 rounded-xl bg-white px-4 py-2 text-sm shadow">
                    <div class="mt-2 text-sm font-semibold">Assistant</div>
                    <div>%s</div>
                    </div>
                """

    if(id == "user_message"):
        Messages += userMessage % (message)
    else:
        Messages += llmMessage % (message)

@sock.route('/echo')
def echo(ws):
    ws.send("<div id=""chat"">%s</div>" % (Messages))
    while True:
        data = ws.receive()
        data_dict = json.loads(data)
        promt = data_dict["user_promt"]
        add_msg(message=promt,id="user_message")
        add_msg(message=comb_instance.run(promt),id="llm_message")
        ws.send("<div id=""chat"">%s</div>" % (Messages))

if __name__ == '__main__':
    app.run()
