from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import hashlib
import requests
from bs4 import BeautifulSoup
from User import User
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)
bcrypt = Bcrypt(app)
# create the database
User.create_table()

API_KEYS = {
    "username": "Hasiru",
    "api_key": "adflj32ojrkwrb23lfs32jks"
}
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
                             api_key=decode_api_key)
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
def get_the_text(id):
    with open('test.txt', 'r') as f:
        data = f.read(int(id))
        return jsonify({"data": data})
        

# protected route
@app.route('/search', methods=['POST'])
@require_api_key
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