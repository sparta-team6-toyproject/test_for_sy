from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.rv3ttod.mongodb.net/test')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/honeymoon", methods=["POST"])
def search_post():

    search_receive = request.form['search_give']

    doc = {'search_list': search_receive}
    db.honeymoon.insert_one(doc)

    return jsonify({'msg': '검색어 리스트 저장 완료!'})


@app.route("/honeymoon", methods=["GET"])
def search_get():
    search_list = list(db.honeymoon.find({}, {'_id': False}))
    return jsonify({'search_list': 'POST 연결 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
