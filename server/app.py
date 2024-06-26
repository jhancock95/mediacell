from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

CORS(app)

@app.route('/')
def home():

    # Get user input through url params
    user_input = request.args.get('user_input')

    # Access file and create dictionaries based on codes and id for reference purposes
    try:
        with open("actions.json", 'r') as file:
            data = json.load(file)

            responses_list = data["actions"]
            codewords = {i["codeword"]:i["id"] for i in responses_list}
            ids = {i["id"]:i["codeword"] for i in responses_list}

    except FileNotFoundError:
        return Response("{'error':'File not found'}", status=500)
    except json.JSONDecodeError:
        return Response("{'error':'Error decoding json'}", status=500)

    # Return the corresponding code or id based on user input
    if user_input.isdigit():
        try:
            code = int(user_input)
            id = codewords[code]
            if id:
                return Response(json.dumps({"data": id}), status=200, mimetype="application/json")
            else:
                return Response('{"error":"No associated ID"}', status=422, mimetype="application/json")
        except (KeyError):
            return Response('{"error":"Invalid code"}', status=422, mimetype="application/json")
        
    else:
        try:
            id = user_input
            code = ids[id]
            if code:
                return Response(json.dumps({"data": code}), status=200, mimetype="application/json")
            else:
                return Response('{"error":"No associated code"}', status=422, mimetype="application/json")
        except (KeyError):
            return Response('{"error":"Invalid ID"}', status=422, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)