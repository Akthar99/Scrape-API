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
            api_key TEXT
                )''')

        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def insert_user(fullname, username, password, user_email, api_key):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (fullname, username, password, user_email, api_key) VALUES (?,?,?,?,?)",
                (fullname, username, password, user_email, api_key))
        conn.commit()
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


