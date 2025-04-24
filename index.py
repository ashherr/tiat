from flask import Flask, jsonify, Response

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response("TIAT Test: The site is working in minimal mode", mimetype="text/plain")

def handler(event, context):
    return app(event, context) 