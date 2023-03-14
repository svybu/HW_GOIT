from flask import Flask, render_template, request
import json
from datetime import datetime
import socket
import threading
import logging
from config import storage_path
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
app_logger.addHandler(stream_handler)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'storage', 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(300), nullable=False)

    @classmethod
    def add_message(cls, time, username, message):
        message = cls(time=time, username=username, message=message)
        db.session.add(message)
        db.session.commit()

with app.app_context():
    db.create_all()

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
    with socket.socket() as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(json.dumps(data).encode())
    return "message has been sent!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

def receive_messages(data):
    if not data:
        app_logger.warning("Received empty data")
        return
    app_logger.info(f"Data received: {data}")
    try:
        messages = json.loads(data.decode())
        app_logger.info(f"Parsed data: {messages}")
        if not isinstance(messages, dict):
            app_logger.error(f"Unexpected data format: expected a dictionary, got {type(messages)}")
            return
        with app.app_context():
            for time, message_data in messages.items():
                if not isinstance(message_data, dict) or 'username' not in message_data or 'message' not in message_data:
                    app_logger.error(f"Invalid message format: {message_data}")
                    continue

                username = message_data['username']
                message = message_data['message']
                data_to_write = {time: {'username': username, 'message': message}}
                with open(os.path.join(storage_path, 'data.json'), 'a') as f:
                    app_logger.info('Data written to JSON file')
                    json.dump(data_to_write, f, indent=4)
                try:
                    Message.add_message(time, username, message)
                    app_logger.info('Data written to DB')
                except Exception as e:
                    app_logger.error(f'Error writing data to DB: {e}')
    except json.JSONDecodeError as e:
        app_logger.error(f"Error decoding JSON data: {e}")
    except Exception as e:
        app_logger.error(f"Error receiving data: {e}")

def run_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            app_logger.info(f"Connected by {addr}")
            with conn:
                try:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        receive_messages(data)
                        app_logger.info('Data was received')
                except KeyboardInterrupt:
                    app_logger.info("Socket server stopped")
                    break
                except Exception as e:
                    app_logger.error(f"Error in socket server: {e}")


def run_app():
    app.run(port=3000)

if __name__ == '__main__':
    threading.Thread(target=run_socket_server).start()
    threading.Thread(target=run_app).start()
