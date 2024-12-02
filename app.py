from flask import Flask, request, jsonify, session
from flask_session import Session
from agent import get_agent_message
import json
from flask import current_app,request
import sys
import os

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the LLM Chatbot!"})

@app.route("/chat", methods=["POST"])
def chat():

    try:
        param=json.loads(request.data)
        query=param['query']

        if query!="":
            response=get_agent_message(query)

            




            if response['answer']=="":
                os._exit(0)
                



            return response
        


        else:
            responses=json.dumps({'Result ': " Retry by entering something","status":"Answers completed"})
    except Exception as e:
        print("error",e)
        response=json.dumps({"result":e,"status":"failed"})
        return response

if __name__ == "__main__":
    app.run(debug=True)
