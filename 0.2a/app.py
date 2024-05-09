#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import threading
import subprocess
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time


"""Welcome to the code!"""
# StrataBytes here! Welcome to the code. Currently, the HeliosCore is a work in progress
#  and is planned to be added onto more and more in the future.

"""Please note..."""
# License: GPLv3
# For the Helios Security Robot CCIC Capstone Project
# Please give credit where its due ;)

"""Other Remarks..."""
#INF - used to give info (lol)
#ERR - used if an error occurs and core + script continue to fuction, but impaired.
#CRIT.ERR - used if the error is so bad that it kills a service or core functionality.
#EVENT - used if a service or core is paused, shut down or something similar (an event that changes the state of da kine)
#WARN - use if somthing is off, but its not the end of the world dispite it causing issues (Multiple Scripts Running, Core slowing down, ect.)
    #Also can be used to get the operators attention,



print("==================================")
print("Helios Core Starting... Please standby...")
print("Ver 0.2 Alpha | @StrataBytes https://helios-project.netlify.app")
print("\nKey:\n[(x)|Core] = Helios Core Server \n[(x)|DS] = Detection Service\n[(x)|VCS] = Voice Command Service")
print("==================================")
time.sleep(2)


print("")

#TODO, refine more of the client integration. (animations, and faces)
#   Another General issue, Make the VCS only transcribe WORDS, for the activation command. Current issue is that it is transcribing phrases and sentances.

#configure logging
logger = logging.getLogger('HeliosCore')
logger.setLevel(logging.DEBUG)

#create handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler('Core.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# Separate process variables for each script
detection_process = None
voice_command_process = None
last_command = None




############################
"""SERVICE STARTER"""
############################

def run_detection_script():
    global detection_process
    if detection_process is not None and detection_process.poll() is None:
        logger.info("[WARN|Core] Detection script already running.")
        return
    detection_process = subprocess.Popen(['python3', 'Services/DigitalEye/main_live_refined.py'])
    logger.info("\n[INF|Core] Detection script started.\nThis may take some time...\n")

def run_voice_command_script():
    global voice_command_process
    if voice_command_process is not None and voice_command_process.poll() is None:
        logger.info("[WARN|Core] Voice command script already running.")
        return
    voice_command_process = subprocess.Popen(['python3', 'Services/HeliosVoice/main.py'])
    logger.info("\n[INF|Core] Voice command script started.\nThis may take some time...\n")

@app.route('/')
def home():
    return render_template('index.html')




############################
"""HELIOS FACE SERVICE"""
############################

#[INF|StrataBytes] this code is the endpoint for detection script's JSON payload. It is then forwarded to the static client via same methods (JS)

#initially set to a default value
current_emotion = "neutral"

@app.route('/update_emotion', methods=['POST'])
def update_emotion():
    global current_emotion  #declare global to modify variable
    data = request.json
    current_emotion = data.get('emotion', 'neutral')  #update the global variable
    #print("===============Core Echo===================")
    print(f"[INFO|Core] Emotion updated to: {current_emotion}")
    return jsonify({"status": "success", "message": f"Emotion updated to {current_emotion}"}), 200
    #print("===========================================\n")

@app.route('/get_emotion')
def get_emotion():
    return jsonify({"emotion": current_emotion})






#############################
"""HELIOS VOICE SERVICE"""
############################


#[INF|StrataBytes] this code is the endpoint for voice commands script's JSON payload. It is then forwarded to the static client via same methoods (JS)

@app.route('/command_executed', methods=['POST'])
def command_executed():
    command_data = request.get_json()
    command = command_data.get('command', 'No command received')
    print(f"[INFO|Flask] Command received: {command}")
    return jsonify({"status": "success", "message": f"Command '{command}' received and executed"}), 200

def update_last_command(new_command):
    global last_command
    last_command = new_command
    print(f"[INFO|Core] Last command updated to: {last_command}")

#flask route to fetch the last command
@app.route('/get_command')
def get_command():
    global last_command
    if last_command is None:
        return "No command received yet", 500
    return last_command, 200


if __name__ == '__main__':
    logger.info("[EVENT|Core] Server starting...")
    thread = threading.Thread(target=run_detection_script, daemon=True)
    threadli = threading.Thread(target=run_voice_command_script, daemon=True)

    threadli.start()
    time.sleep(1)  #sleep for a second
    thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    logger.info("[EVENT|Core] Server shutting down...")

