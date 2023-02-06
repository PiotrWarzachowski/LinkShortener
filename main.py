from flask import Flask, request, redirect, jsonify
import string
import json
import random

app = Flask(__name__)



url_map = json.load(open('database.json'))


def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    if short_code in url_map:
        return generate_short_code()
    return short_code

@app.route("/")
def index():
    return "Basic URL shortener aplication"

"""
    Format for POST request to shorten:
    JSON:
        {'url' : "link to redirect", 'custom' : "" - if random "somestring" - if fixed value}
"""

@app.route("/shorten", methods=["POST"])
def shorten():
    url = request.json['url']
    if (request.json['custom'] == ""):
        short_code = generate_short_code()
        url_map[short_code] = [url, 0]
        with open('database.json', 'w') as json_file:
            json_file.write(json.dumps(url_map, indent=4))
        short_url = request.host_url + short_code
    else:
        short_code = request.json['custom']
        url_map[short_code] = [url, 0]
        with open('database.json', 'w') as json_file:
            json_file.write(json.dumps(url_map, indent=4))
        short_url = request.host_url + short_code

    return short_url

@app.route("/<short_code>")
def redirect_url(short_code):
    if short_code in url_map:
        print(type(request.remote_addr))
        ip_data = json.load(open('ip_database.json'))
        if (request.remote_addr not in ip_data):
            with open('ip_database.json', 'w') as json_file:
                ip_data[request.remote_addr] = 1
                json_file.write(json.dumps(ip_data, indent=4))
            
            url_map[short_code][1]+=1
            with open('database.json', 'w') as json_file:
                json_file.write(json.dumps(url_map, indent=4))
        else:
            ip_data[request.remote_addr]+=1
            with open('ip_database.json', 'w') as json_file:
                json_file.write(json.dumps(ip_data, indent=4))
        return redirect(url_map[short_code][0])
    else:
        return "Error: URL not found", 404
@app.route("/get_views/<short_code>")
def get_views(short_code):
    if short_code in url_map:
        amount_of_views = json.load(open('database.json'))[short_code][1]
        return jsonify({"amount_of_views" : amount_of_views}), 200
    else:
        return "Error: URL not found", 404
    
if __name__ == "__main__":
    app.run(debug=True)