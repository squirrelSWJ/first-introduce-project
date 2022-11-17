from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:alskdjfh@cluster0.geumrbf.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

#클라이언트로 데이터 GET 하는 함수
@app.route("/sung")
def sung_get():
    sung_list = list(db.sung.find({},{'_id':False}))
    return jsonify({'sung':sung_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

#방명록 기록하기 버튼 클릭시 데이터 받고 db에 입력하는 함수
@app.route("/sung", methods=["POST"])
def sung_post():
    name_receive = request.form['name_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    randomNum_receive = request.form['randomNum_give']

    count = list(db.sung.find({}, {'_id': False}))
    num = len(count) + 1

    doc = {
        'name':name_receive,
        'star':star_receive,
        'comment':comment_receive,
        'num':num,
        'randomNum':randomNum_receive
    }
    db.sung.insert_one(doc)

    return jsonify({'msg':'기록완료!'})

#방명록 삭제 버튼 클릭시 데이터 받고 db삭제 하는 함수
@app.route("/sung/delete", methods=["POST"])
def sung_del():
    num_receive = request.form['num_give']
    db.sung.delete_one({'num': int(num_receive)})  #선택한num의 db열 삭제

    count = list(db.sung.find({}, {'_id': False})) #db 총 열의 개수 카운트
    num = len(count) + 1

    db.sung.update_one({'num': num}, {'$set': {'num': int(num_receive)}}) #마지막 열에 있는num을 삭제한 num으로 수정

    return jsonify({'msg': '삭제완료!'})

