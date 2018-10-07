from flask import Flask, request, jsonify, make_response
from flask import abort
import sqlite3
from time import gmtime, strftime

app = Flask(__name__)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name',""),
        'password': request.json['password']
    }
    return jsonify({'status': add_user(user)}), 201

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    a_dict=[]
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

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

def del_user(del_user):
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

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

def list_tweets():
    conn = sqlite3.connect('mydb.db')
    print ("open db good")
    api_list=[]
    cusor = conn.execute("SELECT username, body, tweet_time, id from tweets")
    data = cusor.fetchall()
    if len(data) != 0:
        for row in data:
            tweets = {}
            tweets['Tweet By'] = row[0]
            tweets['Body'] = row[1]
            tweets['Timestamp'] = row[2]
            tweets['id'] = row[3]
            print(tweets)
            api_list.append(tweets)

    conn.close()

    return jsonify({'tweets_list' : api_list})

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweets = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweets['username'] = request.json['username']
    user_tweets['body'] = request.json['body']
    user_tweets['created_at']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()) 
    print (user_tweets)
    return jsonify({'status':add_tweet(user_tweets)}), 200

def add_tweet(new_tweets):
    conn = sqlite3.connect('mydb.db')
    print("opened db good!!")
    cursor=conn.cursor()
    cursor.execute("SELECT * from users where username=? ",   (new_tweets['username'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("INSERT into tweets (username, body, tweet_time)    values(?,?,?)",(new_tweets['username'],new_tweets['body'],     new_tweets['created_at']))
        conn.commit()
        return "SUCCESs"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
