import sqlite3
from getPrediction import get_username

username = get_username()

class favorite_exists_exception(Exception):
    pass

class favorite_not_exists_exception(Exception):
    pass

connection = None
cursor = None

def load_db():
    global connection, cursor
    connection = sqlite3.connect('favs.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_favs
                      (username TEXT NOT NULL UNIQUE, favs TEXT)''')
    connection.commit()

def add_favorite(favorite):
    favorites_list = get_favorites()

    if len(favorites_list) == 0:
        # Insert new row
        cursor.execute("INSERT INTO user_favs (username, favs) VALUES (?, ?)", (username, favorite))
    if favorite in favorites_list:
        raise favorite_exists_exception()
    else:
        # Update favorites
        favorites_list.append(favorite)
        cursor.execute("UPDATE user_favs SET favs=? WHERE username=?", (','.join(favorites_list), username))
    connection.commit()

def remove_favorite(favorite):
    favorites_list = get_favorites()

    if len(favorites_list) == 0:
        return

    if favorite not in favorites_list:
        raise favorite_not_exists_exception()
    else:
        favorites_list.remove(favorite)
        cursor.execute("UPDATE user_favs SET favs=? WHERE username=?", (','.join(favorites_list), username))
    connection.commit()

def get_favorites():
    cursor.execute("SELECT favs FROM user_favs WHERE username=?", (username,))
    row = cursor.fetchone()
    if row:
        favorites = row[0]
        if favorites:
            return favorites.split(',')
    return []

def close():
    connection.close()


