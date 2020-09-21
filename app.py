from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from pymongo import MongoClient
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from multiprocessing import Value

counter = Value('i', 0)
counter2 = Value('i', 0)
counter3 = Value('i', 0)

app = Flask(__name__)
app.config['SECRET_KEY']  = '5791628bb0b13ce0c676dfde280ba245'
#app.config['MONGO_DBNAME'] = 'bktlist'
client =MongoClient('mongodb+srv://User_1:Qwerty@cluster0.q5slf.mongodb.net/bktlist?retryWrites=true&w=majority')

abc=client.bktlist.abc

@app.route('/')
def index():
    if 'username' in session:
        return render_template('stories.html')

    return render_template('index.html')
    
@app.route('/story1',methods=['GET', 'POST'])
def story1():
    with counter.get_lock():
        counter.value += 1
        out = counter.value
    print("count = ",out)
    return render_template('story_1.html',variable=out)


@app.route('/story2',methods=['GET', 'POST'])
def story2():
    with counter2.get_lock():
        counter2.value += 1
        out2 = counter2.value
    print("count = ",out2)
    return render_template('story_2.html',variable=out2)        


@app.route('/story3',methods=['GET', 'POST'])
def story3():
    with counter3.get_lock():
        counter3.value += 1
        out3 = counter3.value
    print("count = ",out3)
    return render_template('story_3.html',variable=out3)

@app.route('/login', methods=['POST'])
def login():
    users=abc
    login_user = users.find_one({'name': request.form['username']})
    #print(login_user)
    if login_user:
        if check_password_hash(login_user['password'],request.form['pass']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username or password.. Please go back and try again.'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = abc
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['pass'],'sha256')
            users.insert({'name':request.form['username'], 'password': hashpass})
            session['username'] =  request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Please go back and register again'

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
