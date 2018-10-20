from flask import Flask, request, jsonify, flash
from flask import abort
from flask import make_response, url_for
import json
from time import gmtime, strftime
import sqlite3
from flask import render_template
from flask_cors import CORS, cross_origin 
from flask import redirect, session
from flask import current_app
import flask
from pymongo import MongoClient
import random
import bcrypt

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

def list_users():
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully")
    api_list=[]
    cursor = conn.execute("SELECT username, full_name,  email, password, id from users")
    for row in cursor:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['name'] = row[1]
        a_dict['email'] = row[2]
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]
        api_list.append(a_dict)

    conn.close()
    return jsonify({'user_list': api_list})
    """

    api_list = []
    db = connection.cloud_native.users
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'user_list' : api_list})

def list_user(user_id):
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where id=?",(user_id,))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:

        user = {}
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id'] = data[0][4]

    conn.close()
    return jsonify(user)
    """
    api_list=[]
    db = connection.cloud_native.users
    for i in db.find({'id':user_id}):
        api_list.append(str(i))

    if api_list == []:
        abort(404)

    return jsonify({'user_details': api_list})


def list_tweet(user_id):
    print (user_id)
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from tweets  where id=?",(user_id,))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:

        user = {}
        user['id'] = data[0][0]
        user['username'] = data[0][1]
        user['body'] = data[0][2]
        user['tweet_time'] = data[0][3]

    conn.close()
    return jsonify(user)

def add_user(new_user):
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? or email=?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
       cursor.execute("insert into users (username, email, password, full_name) values(?,?,?,?)",(new_user['username'],new_user['email'], new_user['password'], new_user['name']))
       conn.commit()
       return "Success"
    conn.close()
    return jsonify(a_dict)
    """
    api_list = []
    print(new_user)
    db = connection.cloud_native.users
    user = db.find({'$or': [
        {
            "username": new_user['username']
        },
        {
            "email": new_user['email']
        }
    ]
    })
    for i in user:
        print (str(i))
        api_list.append(str(i))

    if api_list == []:
        db.insert(new_user)
        return "success"
    else:
        abort(409)

def del_user(del_user):
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? ",(del_user,))
    data = cursor.fetchall()
    print ("Data" ,data)
    if len(data) == 0:
        abort(404)
    else:
       cursor.execute("delete from users where username==?",(del_user,))
       conn.commit()
       return "Success"
    """

    db = connection.cloud_native.users
    api_list = []
    for i in db.find({ 'username': del_user}):
        api_list.append(str(i))

    if api_list == []:
        abort(404)
    else:
        db.remove({"username": del_user})
        return "success"

def list_tweets():
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT username, body, tweet_time, id from tweets")
    data = cursor.fetchall()
    print (data)
    print (len(data))
    if len(data) == 0:
        return api_list
    else:
        for row in data:
            tweets = {}

            tweets['tweetedby'] = row[0]
            tweets['body'] = row[1]
            tweets['timestamp'] = row[2]
            tweets['id'] = row[3]

            print (tweets)
            api_list.append(tweets)

    conn.close()
    print (api_list)
    return jsonify({'tweets_list': api_list})
    """

    api_list=[]
    dict = {}
    db = connection.app.tweets
    for row in db.find():
        print (row)
        dict = {}
        dict['id'] = row['id']
        dict['timestamp'] = row['timestamp']
        dict['tweetedby'] = row['tweetedby']
        dict['body'] = row['body']
        api_list.append(dict)

    print (api_list)
    return json.dumps(api_list)

def add_tweet(new_tweet):
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? ",(new_tweets['username'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
       cursor.execute("INSERT into tweets (username, body, tweet_time) values(?,?,?)",(new_tweets['username'],new_tweets['body'], new_tweets['created_at']))
       conn.commit()
       return "Success"
    """
    api_list=[]
    print (new_tweet)
    db_user = connection.app.users
    db_tweet = connection.app.tweets

    user = db_user.find({"username":new_tweet['tweetedby']})
    for i in user:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
        db_tweet.insert(new_tweet)
        return "Success"    

def upd_user(user):
    '''
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where id=? ",(user['id'],))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
        abort(404)
    else:
        key_list=user.keys()
        for i in key_list:
            if i != "id":
                print (user, i)
                # cursor.execute("UPDATE users set {0}=? where id=? ", (i, user[i], user['id']))
                cursor.execute("""UPDATE users SET {0} = ? WHERE id = ?""".format(i), (user[i], user['id']))
                conn.commit()
    return "Success"
    '''

    api_list=[]
    print(user)

    db_user = connection.cloud_native.users
    users = db_user.find_one({"id": user['id']})
    for i in users:
        api_list.append(str(i))

        if api_list == []:
            abort(409)
        else:
            db_user.update({'id':user['id']}, {'$set': user}, upsert=False)
            return "Success"


@app.route("/api/v1/info")
def home_index():
    """
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor = conn.execute("SELECT buildtime, version, methods, links from apirelease")
    for row in cursor:
        api = {}
        api['version'] = row[0]
        api['buildtime'] = row[1]
        api['methods'] = row[2]
        api['links'] = row[3]
        api_list.append(api)
    conn.close()
    """

    api_list=[]
    db = connection.cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))

    return jsonify({'api_version': api_list}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    print("json:{}".format(request.json))
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name',""),
        'password': request.json['password']
    }
    user['id'] = random.randint(1,1000)

    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    # if not request.json:
    #     abort(400)
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print (user)

    return jsonify({'status': upd_user(user)}), 200





@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():

    print("add_tweets:{}".format(request.json))

    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['tweetedby'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['timestamp']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    user_tweet['id'] = random.randint(1,1000)

    return  jsonify({'status': add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

#starting chapter 3 stuff

@app.route('/adduser')
def adduser():
    #return render_template('adduser2.html') 
    return render_template('adduser3.html') 

@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')

@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        #Add then redirect the user to the main page
        return redirect(url_for('main'))
    else:
        return render_template('addname.html', session=session)

@app.route('/clear')
def clearsession():
    #clear the session
    session.clear()
    #redirect to main
    return redirect(url_for('main'))

@app.route('/set_cookie')
def cookie_insertion():
    redirect_to_main = redirect('/')
    response = current_app.make_response(redirect_to_main)
    response.set_cookie('cookie_name', value='values')
    return response

#chapter 4 stuff
connection = MongoClient("mongodb://localhost:27017")
def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease

            db.insert({
                "email": "eric.strom@google.com",
                "id":33,
                "name": "Eric stromberg", 
                "password": "eric@123", 
                "username": "eric.strom"
            })

            db_tweets.insert({
                "body": "New blog post,Launch your app with the AWS Startup Kit! #AWS",
                "id": 18, 
                "timestamp": "2017-03-11T06:39:40Z", 
                "tweetedby": "eric.strom" 
            })

            db_api.insert( { 
                "buildtime": "2017-01-01 10:00:00", 
                "links": "/api/v1/users", 
                "methods": "get, post, put, delete", 
                "version": "v1" 
            }) 
            db_api.insert( { 
                "buildtime": "2017-02-11 10:00:00", 
                "links": "api/v2/tweets", 
                "methods": "get, post", 
                "version": "2017-01-10 10:00:00" 
            })
            
            print ("Database Initialize completed!") 
        else: 
            print ("Database already Initialized!")
    except: 
        print ("Database creation failed!!") 

#chapter 5
@app.route('/index')
def index():
    return render_template('index.html')

def main(): 
    cookie_name = flask.request.cookies.get('cookie_name')
    print("cookie:{}".format(cookie_name))
    return render_template('main.html') 

@app.route('/') 
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', session = session['username'])

@app.route('/login', methods=['POST'])
def do_admin_login():
    users = connection.cloud_native.users
    api_list=[]
    login_user=users.find({ 'username' : request.form['username']})
    for i in login_user:
        api_list.append(i)
    print(api_list)
    if api_list != []:
        db_password = api_list[0]['password'].decode('utf-8')
        form_password = request.form['password'].encode('utf-8')
        hashed_form_password = bcrypt.hashpw(request.form['password'].encode('utf-8'),
                                             api_list[0]['password']).decode('utf-8')
        print("db password:{}".format(db_password))
        print("form password:{}".format(form_password))
        print("form hashed password:{}".format(hashed_form_password))

        if db_password == hashed_form_password:
            session['logged_in'] = api_list[0]['username']
            return redirect(url_for('index'))
    else:
        flash("Invalid Authentication")

    return "Invalid User!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = connection.cloud_native.users
        api_list=[]
        existing_user = users.find({ '$or': [
            {
                "username": request.form['username']
            },
            {
                "email": request.form['email']

            }]
        })
        for i in existing_user:
            api_list.append(str(i))
        if api_list == []:
            users.insert({
                "email":request.form['email'],
                "id":random.randint(1,1000),
                "name":request.form['name'],
                "password":bcrypt.hashpw(request.form['pass'].encode('utf-8'),
                                         bcrypt.gensalt()),
                "username":request.form['username']
            })
            session['username'] = request.form['username']
            return redirect(url_for('home'))

        return 'That user already exists'
    else:
        return  render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = connection.cloud_native.users
    existing_users = users.find({
        "username" : session['username']
    })
    if request.method=='POST':
        api_list=[]

        for i in existing_users:
            api_list.append(str(i))
        user = {}
        print(api_list)
        if api_list != []:
            print (request.form['email'])
            user['email'] = request.form['email']
            user['name']= request.form['name'] 

            plain_pass = request.form['pass']
            encrypted = bcrypt.hashpw(plain_pass.encode('utf-8'), bcrypt.gensalt())

            user['password']=encrypted
            users.update(
                {
                    'username' : session['username'],
                },
                {
                    '$set' : user
                }
            )
        else:
            return 'User not found!'

        return redirect(url_for('index'))
    elif request.method=='GET':
        user = []
        print (session['username'])
        for i in existing_users: 
            user.append(i)       
        print (user[0])  
        return render_template('profile.html',
            name=user[0]['name'],
            username=user[0]['username'],
            password=user[0]['password'],
            email=user[0]['email'])

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_mongodatabase() 
    app.run(host='0.0.0.0', port=5000, debug=True)
