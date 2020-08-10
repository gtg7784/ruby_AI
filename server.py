import argparse
import json
from flask import Flask, request, Response, make_response
from train import KoGPT2Chat

parser = argparse.ArgumentParser(description='Ruby based on KoGPT-2')
args = parser.parse_args()
model = KoGPT2Chat.load_from_checkpoint(args.model_params)
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = {"msg": model.chat(request.form['sentence'])}
    r = make_response(data)
    r.mimetype = 'application/json'
    return r

print("The WebServer is online!")
app.run(host='0.0.0.0', port=80)