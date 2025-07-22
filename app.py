from flask import Flask, request, jsonify
from agent import get_agent_message
import json

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Aged Care/Disability HRM Chatbot!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        param = request.get_json()
        query = param.get('query', '')

        if query:
            response = get_agent_message(query)
            if response['answer'] == "":
                return jsonify({'result': "All questions answered. Thank you!", "status": "completed"})
            return jsonify(response)
        else:
            return jsonify({'result': "Retry by entering something", "status": "Answers completed"})
    except Exception as e:
        print("error", e)
        return jsonify({"result": str(e), "status": "failed"})

if __name__ == "__main__":
    app.run(debug=True)
