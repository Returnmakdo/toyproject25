from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://Test999:Sparta9*@cluster0.mc4ytkq.mongodb.net/?retryWrites=true&w=majority')
# db = client.dbsparta

@app.route('/')
def home():
    return render_template('Sign_up.html')

@app.route("/sign_up", methods=["POST"])
def Sign_up_post():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    cpw_receive = request.form['cpw_give']

    doc = {
        'name':name_receive,
        'email':email_receive,
        'pw':pw_receive,
        'cpw':cpw_receive
    }
    db.Sign_up.insert_one(doc)

    return jsonify({'msg':'Register Complete!!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)




