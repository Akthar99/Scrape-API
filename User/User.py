import sqlite3

def create_table():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            username TEXT,
            password TEXT,
            user_email TEXT,
            api_key TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            card TEXT
                )''')

        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# create a new table for the subscription
def create_subciption_tabse():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS subscription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subscription_plan TEXT,
            request INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
                  )''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def create_card_information_table():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS card_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            card_name TEXT,
            card_number TEXT,
            expiry_month TEXT,
            expiry_year TEXT,
            card_cvv TEXT,
            card_type TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
                  )''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# get the subscription by api key
def get_subscription_plan_(api_key):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE api_key =?", (api_key,))
        result = c.fetchone()
        if result is None:
            conn.close()
            return False
        elif result:
            # check the subcription table where users id is user_id in the table and get the subcription
            c.execute("SELECT subscription_plan FROM subscription WHERE user_id =?", (result[0],))
            subscription = c.fetchone()
            if result:
                conn.close()
                return subscription
            else:
                conn.close()
                return False
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# get the id of the user from username 
def get_user_id(username):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username =?", (username,))
        result = c.fetchone()
        if result:
            conn.close()
            return result[0]
        else:
            conn.close()
            return False
    except sqlite3.Error as e:
        print(e)

# get the username by api key

def get_username_by_api_key(api_key):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE api_key =?", (api_key,))
        result = c.fetchone()
        if result:
            conn.close()
            return result[2]
        else:
            conn.close()
            return False
    except sqlite3.Error as e:
        print(e)

# create a new user 
def insert_user(fullname, username, password, user_email, api_key, subscription_plan):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (fullname, username, password, user_email, api_key) VALUES (?,?,?,?,?)",
                (fullname, username, password, user_email, api_key))
        conn.commit()
        user_id = get_user_id(username=username)
        c.execute("INSERT INTO subscription (user_id, subscription_plan) VALUES (?,?)",
                (user_id, subscription_plan))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    
# get the api key with the username and password
def get_api_key(username):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username =?", (username,))
        result = c.fetchone()
        if result:
            conn.close()
            return result[5], result[3]
        else:
            conn.close()
            return False, False
    except sqlite3.Error as e:
        print(e)


def authenticate_api_key(api_key):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE api_key = ?", (api_key,))
        result = c.fetchone()
        if result is None:
            conn.close()
            return False
        else:
            conn.close()
            return True
    except sqlite3.Error as e:
        print(e)

# see if the user already exists in the database
def check_user(username):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        
        if result:
            return result[2]  # Returning the username if found
        else:
            return None  # Returning None if username doesn't exist
    
    except sqlite3.Error as e:
        print("An error occurred while checking user:", e)
        return None  # Returning None in case of an error

# Check if the 24 hours have passed since

def get_date_by_username_or_api_key(api_key=None, username=None):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT date FROM users WHERE username =? OR api_key =?", (username, api_key))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]  # Returning the username if found
        else:
            return None  # Returning None if username doesn't exist
    except sqlite3.Error as e:
        print("An error occurred while checking user:", e)
        return None  # Returning None in case of an error

def update_date_by_username_or_api_key(username=None, api_key=None):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE users SET date = CURRENT_TIMESTAMP WHERE username =? OR api_key =?", (username, api_key))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred while checking user:", e)
        return None  # Returning None in case of an error

def get_request_by_api_key(api_key=None, username=None):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username =? OR api_key =?", (username, api_key))
        id_ = c.fetchone()
        c.execute("SELECT request FROM subscription WHERE user_id =?", (id_[0],))
        request = c.fetchone()
        conn.close()
        if request:
            return request[0]  # Returning the request if found
        else:
            return None  # Returning None if request doesn't exist
    except sqlite3.Error as e:
        print("An error occurred while checking user:", e)
        return None  # Returning None in case of an error

# update the request by api_key
def update_request_by_api_key(api_key):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE api_key =?", (api_key,))
        id_ = c.fetchone()
        c.execute("UPDATE subscription SET request = request + 1 WHERE user_id = ?", (id_[0],))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred while checking user:", e)
        return None  # Returning None in case of an error

# reset the request by api key
def reset_request_by_api_key(api_key):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE api_key =?", (api_key,))
        id_ = c.fetchone()
        c.execute("UPDATE subscription SET request = 0 WHERE user_id = ?", (id_[0],))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("An error occurred while checking user:", e)

# get and insert card information to the databse 
def get_card(api_key):
    """return the card information from the database by api key"""
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE api_key =?", (api_key,))
        id_ = c.fetchone()
        if id_:
            c.execute("SELECT * FROM card_information WHERE user_id =?", (id_[0],))
            result = c.fetchone()
            if result:
                conn.close()
                return result
            else:
                conn.close()
                return False
        else:
            conn.close()
            return False
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

# insert the information to the card_information table 

def insert_card(api_key, card_name, card_number, expiry_month, expiry_year, card_cvv, card_type):
    """
    Insert card information to the card_information table
    """
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE api_key =?", (api_key,))
        id_ = c.fetchone()
        if id_:
            c.execute("""INSERT INTO card_information (user_id, card_name, card_number, expiry_month,
                      expiry_year, card_cvv, card_type) VALUES (?,?,?,?,?,?,?)""",
                    (id_[0], card_name, card_number, expiry_month, expiry_year, card_cvv, card_type))
            conn.commit()
            conn.close()
            return True
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def check_card(card_number, user_id):
    """check if the card number is aleady available in the database"""
    try:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT user_id FROM card_information WHERE card_number =? or user_id =?", (card_number, user_id))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print(e)


get_card.__doc__ = """return the card information from the database by api key"""