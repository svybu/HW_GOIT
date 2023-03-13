from flask import Flask, render_template, request
import json
import os
from datetime import datetime
import socket
import threading
from config import storage_path

app = Flask(__name__)
server_address = ('localhost', 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('message.html')

@app.route('/message', methods=['POST'])
def process_message():
    username = request.form['username']
    message = request.form['message']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {time: {'username': username, 'message': message}}
    sock.sendto(json.dumps(data).encode(), server_address)
    return "message has been sent!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


def receive_messages():
    while True:
        data, address = sock.recvfrom(4096)
        messages = json.loads(data.decode())
        for time, message in messages.items():
            print(f"[{time}] {message['username']}: {message['message']}")
            data_to_write = {time: {'username': message['username'], 'message': message['message']}}
            with open(os.path.join(storage_path, 'data.json'), 'a') as f:
                json.dump(data_to_write, f, indent=4)
            #sock.sendto(b"Data received", address)


if __name__ == '__main__':
    threading.Thread(target=receive_messages).start()
    app.run(debug=True, port=3000)

