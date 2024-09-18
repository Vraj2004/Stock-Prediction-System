import sqlite3

class user_not_exists_exception(Exception):
    pass

class password_mismatch_exception(Exception):
    pass

class favorite_exists_exception(Exception):
    pass

class favorite_not_exists_exception(Exception):
    pass

# Global variables for database connections
favs_db = None
favs_cursor = None
users_db = None
users_cursor = None

def load_db():
    global favs_db, favs_cursor
    favs_db = sqlite3.connect('favs.db')
    favs_cursor = favs_db.cursor()
    favs_cursor.execute('''CREATE TABLE IF NOT EXISTS user_favs
                          (username TEXT NOT NULL UNIQUE, favs TEXT)''')
    favs_db.commit()
    global users_db, users_cursor
    users_db = sqlite3.connect('users.db')
    users_cursor = users_db.cursor()
    users_cursor.execute('''CREATE TABLE IF NOT EXISTS auth
                              (username TEXT NOT NULL UNIQUE, password TEXT)''')
    users_db.commit()

def is_user(username):
    users_cursor.execute("SELECT 1 FROM auth WHERE username=?", (username,))
    exists = users_cursor.fetchone() is not None
    return exists

def match_password(username, password):
    if not is_user(username):
        raise user_not_exists_exception(f"User {username} is not registered for Stock Predictor!")

    users_cursor.execute("SELECT password FROM auth WHERE username=?", (username,))
    row = users_cursor.fetchone()

    if row:
        stored_password = row[0]
        if stored_password == password:
            return True
        else:
            raise password_mismatch_exception("Password does not match!")
    else:
        raise user_not_exists_exception(f"No such user found: {username}")

def register_user(username, password):
    if is_user(username):
        raise user_not_exists_exception(f"User {username} is already registered for Stock Predictor!")

    users_cursor.execute("INSERT INTO auth (username, password) VALUES (?, ?)", (username, password))
    users_db.commit()


def add_favorite(username, favorite):
    favorites_list = get_favorites(username)

    if favorite in favorites_list:
        raise favorite_exists_exception(f"Stock {favorite} is already in your favorites!")

    # Append the new favorite to the list
    favorites_list.append(favorite)

    # Update the favorites in the database
    favs_cursor.execute("INSERT OR REPLACE INTO user_favs (username, favs) VALUES (?, ?)",
                        (username, ','.join(favorites_list)))
    favs_db.commit()

def is_favorite(username, favorite):
    return favorite in get_favorites(username)

def remove_favorite(username, favorite):
    favorites_list = get_favorites(username)

    if favorite not in favorites_list:
        raise favorite_not_exists_exception(f"Stock {favorite} is not in your favorites!")

    # Remove the favorite from the list
    favorites_list.remove(favorite)

    # Update the favorites in the database
    favs_cursor.execute("UPDATE user_favs SET favs=? WHERE username=?",
                        (','.join(favorites_list), username))
    favs_db.commit()

def get_favorites(username):
    favs_cursor.execute("SELECT favs FROM user_favs WHERE username=?", (username,))
    row = favs_cursor.fetchone()

    if row and row[0]:
        return row[0].split(',')
    return []

def close_db():
    if favs_db:
        favs_db.close()
    if users_db:
        users_db.close()
