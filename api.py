from flask import Flask, request, jsonify
from flask_cors import CORS
from run_conversation import build_bots, run_conversation
import os
import subprocess

app = Flask(__name__)
CORS(app)

# Optional: Only allow your WordPress domain (safer in production)
# CORS(app, resources={r"/run-conversation": {"origins": "https://your-wordpress-site.com"}})

@app.route('/run-conversation', methods=['POST'])
def api_run_conversation():
    
    print("Current working directory:", os.getcwd())
    dumb, smart = build_bots()
    start_message = "Hello"
    rounds = 6
    log_to_file = True
    extension = 'md'
    
    try:
        conversation_output = run_conversation(
            dumb=dumb,
            smart=smart,
            start_message=start_message,
            rounds=rounds,
            log_to_file=log_to_file,
            extension=extension
        )
        return jsonify({"status": "success", "conversation": conversation_output})    # Should be stored in ./bots/log
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    



@app.route('/run-prebuilt', methods=['GET'])
def run_script():
    try:
        # Run the script as a subprocess
        # Make sure the path is correct relative to where Flask is running
        result = subprocess.run(
            ['python', 'prebuilt/run.py'],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({
            "status": "success",
            "output": result.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "output": e.stderr
        }), 500

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
