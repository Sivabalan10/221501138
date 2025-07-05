from flask import Flask, request, jsonify, redirect
from service import shorten_url
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the URL Shortener API"}), 200


@app.route("shorturls", methods=["POST"])
def shorten_url_route():
    data = request.json
    long_url = data.get('url')

    if not long_url:
        return jsonify({"error": "No URL provided"}), 400

    short_url = shorten_url(long_url)
    return jsonify({"shortened_url": short_url}), 200

