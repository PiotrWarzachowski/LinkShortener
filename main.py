from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import re
import string
import json
import random
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


url_map = json.load(open('database.json'))


def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(8))
    if short_code in url_map:
        return generate_short_code()
    return short_code

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        url = request.form['url']
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(regex, url) is None:
            flash('The URL is not valid. Enter URL in this format : https://example.com')
            return redirect(url_for('index'))
        elif not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        if request.form['custom_link'] != "":
            customlink = os.environ['WEBSITE_URL'] + request.form['custom_link']
            print(customlink)
            return render_template('index.html', short_url=customlink)
        else:
            customlink = os.environ['WEBSITE_URL'] + generate_short_code()
            print(customlink)
            return render_template('index.html', short_url=customlink)
        print(url)
    
    return render_template('index.html')


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

@app.route("/<short_code>/statistics")
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


    
if __name__ == "__main__":
    app.run(debug=True, port=1111)