from bson import json_util
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.rv3ttod.mongodb.net/test')
db = client.hanghae_10_preliminary
sparta = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list')
def list():
    return render_template('2.html')


@app.route('/travel', methods=["GET"])
def list_get():
    cities = ['루체른', '마드리드', '로마', '아테네', '파리',
              '하와이', '칸쿤', '뉴욕', '몰디브', '발리', '보라카이', '세부', '다낭']
    results = []
    for city in cities:
        result = db.travel.find_one({'city_kor': city}, {'_id': False})
        results.append(result)
    return jsonify(results)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
