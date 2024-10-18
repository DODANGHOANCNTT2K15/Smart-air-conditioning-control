from flask import Flask, jsonify, request
import config
import importlib  

app = Flask(__name__)

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    importlib.reload(config)  
    return jsonify({"temperature": config.temperature})

@app.route('/set_temperature', methods=['POST'])
def set_temperature():
    new_data = request.json
    config.temperature = new_data.get('temperature', config.temperature)  
    return jsonify({"temperature": config.temperature})

def run_flask():
    app.run(host='0.0.0.0', port=5000)
