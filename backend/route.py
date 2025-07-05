from flask import Flask, request, jsonify, redirect
from service import shorten_url
from db import init_db, insert_url, get_url, insert_stat, get_stats
from flask_cors import CORS
from dotenv import load_dotenv
from handler import log

load_dotenv()

app = Flask(__name__)
CORS(app)
init_db()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the URL Shortener API"}), 200

@app.route("/shorturls", methods=["POST"])
def shorten_url_route():
    data = request.json
    long_url = data.get('url')
    validity = data.get('validity', 30)
    shortcode = data.get('shortcode')

    if not long_url:
        log("No URL provided", level="error", package="route")
        return jsonify({"error": "No URL provided"}), 400

    try:
        code, expiry = shorten_url(long_url, validity, shortcode)
        insert_url(long_url, code, validity, expiry)
        # Build the full short URL
        short_url_full = request.host_url.rstrip('/') + '/r/' + code
        return jsonify({"shortLink": short_url_full, "expiry": expiry}), 200
    except Exception as e:
        log(f"Shorten URL error: {str(e)}", level="error", package="route")
        return jsonify({"error": str(e)}), 400

@app.route("/shorturl/<short_url_link>", methods=["GET"])
def short_url_stats(short_url_link):
    url_row = get_url(short_url_link)
    if not url_row:
        log(f"Short URL not found: {short_url_link}", level="error", package="route")
        return jsonify({"error": "Short URL not found"}), 404
    stats = get_stats(short_url_link)
    response = {
        "created_time": url_row[1],
        "longurl": url_row[2],
        "shorturl": url_row[3],
        "validity": url_row[4],
        "expiry": url_row[5],
        "clicks": stats
    }
    return jsonify(response), 200

@app.route("/r/<shortcode>", methods=["GET"])
def redirect_short_url(shortcode):
    url_row = get_url(shortcode)
    if not url_row:
        log(f"Short URL not found for redirect: {shortcode}", level="error", package="route")
        return jsonify({"error": "Short URL not found"}), 404
    try:
        insert_stat(shortcode, url_row[2], request.remote_addr)
    except Exception as e:
        log(f"Insert stat error: {str(e)}", level="error", package="route")
    return redirect(url_row[2])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)