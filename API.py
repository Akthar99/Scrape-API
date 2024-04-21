from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import hashlib
import requests
from bs4 import BeautifulSoup
from User import User
from cryptography.fernet import Fernet
import base64
import pandas as pd
import time

app = Flask(__name__)
bcrypt = Bcrypt(app)
# create the database
User.create_table()
# create the subcription table
User.create_subciption_tabse()


# check the database if the api key is valid
def authenticate_api_key(api_key):
    return User.authenticate_api_key(api_key)

# decorator for authenticate_api_key 
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return jsonify({'authenticated': False,
                            'help': 'not api-key found in your request you might want to register first'}), 401
        elif not authenticate_api_key(api_key):
            return jsonify({'authenticated': False,
                            'help': 'api-key you suplied is wrong'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# check if the user is subscribed to the service
def subscription_requiere(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        isVaild = authenticate_api_key(api_key)
        if isVaild:
            # get the subscription plan from the subscription table
            subscription_plan = User.get_subscription_plan(api_key)
            if subscription_plan:
                return func(*args, **kwargs)
            else:
                return jsonify({'authenticated': False,
                                'help': 'you are not subscribed yet'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
    
# limit the number of requests per day acording to the subscription they using 
def subscription_limit(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        isVaild = authenticate_api_key(api_key)
        if isVaild:
            # get the subscription plan from the subscription table
            subscription_plan = User.get_subscription_plan(api_key)
            if subscription_plan[0] == "free":
                with open("free.csv", "a") as log_file:
                    log_file.writelines(f"{User.get_username_by_api_key(api_key)},{str(request.remote_addr)},{time.ctime()} \n")
                    log_file.close()
                # check if the 24 hour is passed in
                date = User.get_date_by_username_or_api_key(api_key)
                timestamp = time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S"))
                time_deference = time.time() - timestamp
                requests_ = User.get_request_by_api_key(api_key)
                if date:
                    if time_deference >= 86400:
                        User.update_date_by_username_or_api_key(api_key)
                    elif requests_ >= 10:
                        return jsonify({'authenticated': False,
                                    'help': 'your request per day is over! please subscribe to other subscription plan if you wants'}), 401
                    else:
                        User.update_request_by_api_key(api_key)
                        return func(*args, **kwargs)
            else:
                return jsonify({'authenticated': False,
                                'help': 'your request per day is over! please subscribe to other subscription plan if you wants'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data['full_name']
    username = data['username']
    password = data['password']
    user_email = data['user_email']
    api_key = Fernet.generate_key()
    decode_api_key = base64.urlsafe_b64encode(api_key).decode('utf-8')
    userIsvaild = User.check_user(username)
    if data:
        if not username:
            return jsonify({'authenticated': False,
                            'help': 'username is invaild'}), 400
        elif userIsvaild:
            return jsonify({'authenticated': False,
                            'help': 'username is already exists registered'}), 400
        elif not password:
            return jsonify({'authenticated': False,
                            'help': 'password is invaild'}), 400
        elif not user_email:
            return jsonify({'authenticated': False,
                            'help': 'email is invaild'}), 400
        elif not userIsvaild:
            User.insert_user(username=username, fullname=full_name,
                             password=bcrypt.generate_password_hash(password).decode('utf-8'),
                             user_email=user_email,
                             api_key=decode_api_key,
                             subscription_plan='free')
            return jsonify({'authenticated': True}), 200
        

# Get the api key with username and password
@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data['username']
    password = data['password']
    api_key, hash_password = User.get_api_key(username=username)
    if api_key:
        isAuthenticated = bcrypt.check_password_hash(hash_password, password)
        if isAuthenticated:
            return jsonify({'authenticated': True,
                            'api_key': api_key}), 200
        else:
            return jsonify({'authenticated': False,
                            'help': 'must be password is incorrect'}), 401
    else:
        return jsonify({'authenticated': False}), 401


# protected route
@app.route('/get-data/<id>', methods=['GET'])
@require_api_key
@subscription_requiere
@subscription_limit
def get_the_text(id):
    with open('test.txt', 'r') as f:
        data = f.read(int(id))
        return jsonify({"data": data})
        

# protected route
@app.route('/search', methods=['POST'])
@require_api_key
@subscription_limit
def search():
    data = request.get_json()
    search_text = data['search_text']
    pull = data['pull'] if 'pull' in data else 5

    res = requests.get(f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit={pull}&offset=0&ns0=1&search={search_text}")
    content = res.text

    soup = BeautifulSoup(content, 'lxml')
    tags = soup.find_all('div', class_="searchresult")
    links = soup.find_all("a")

    results = []
    for link in links:
        extracted_link = link.get("href")
        if extracted_link.startswith('http'):
            results.append({'link': extracted_link})

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)


'''
[ ALL THE ROUTERS ]

/register 
/get-data/<id>
/search
/authenticate

'''