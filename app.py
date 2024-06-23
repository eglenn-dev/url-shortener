from flask import Flask, render_template, redirect, request, send_from_directory, send_file, jsonify
import string
import random
import db_model as db

app = Flask(__name__, static_url_path='/web', static_folder='web')

@app.route('/')
def index():
    return send_file('web/pages/index.html')

@app.route('/api', methods=['GET', 'POST'])
def api():
    return redirect('/')

@app.route('/api/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    short = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    print(f'Generated short URL: {short}')
    while True:
        if db.check_exists(short):
            short = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        else:
            db.write(short, url)
            return jsonify({'shortUrl': short}), 200

@app.route('/api/stats', methods=['POST'])
def stats():
    data = request.get_json()
    short = data.get('shortUrl')
    if not short:
        return jsonify({'error': 'Short URL not provided'}), 400
    if db.check_exists(short):
        stats = {}
        stats['clickCount'] = db.get_stats(short)
        stats['originalUrl'] = db.read_one(short)
        stats['shortUrl'] = short
        return jsonify({'stats': stats}), 200
    else:
        return jsonify({'error': 'Short URL not found'}), 404

@app.route('/<short>')
def redirect_short(short):
    if db.check_exists(short):
        url = db.read_one(short)
        db.log_stats(short)
        return redirect(url)
    else:
        return jsonify({'error': 'Short URL not found'}), 404

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == '__main__':
    app.run(port=5510, debug=True) # For debugging
    # app.run(port=5500, host='0.0.0.0') # For deployment