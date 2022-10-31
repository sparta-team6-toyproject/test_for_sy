
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.rv3ttod.mongodb.net/test')
db = client.hanghae_10_preliminary


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list')
def list():
    return render_template('2.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
