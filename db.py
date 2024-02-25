def connect_to_database(name="database.db"):
    import sqlite3

    return sqlite3.connect(name, check_same_thread=False)

# Users 
def init_users(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL,
        admin TEXT NOT NULL,
        dob date,
        profile_photo BLOB
        )   
        """
    )

    connection.commit()

def add_user(connection, username, password,dob,profile_photo):
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password,admin,dob,profile_photo) VALUES (?, ?,?,?,?)"
    cursor.execute(query, (username, password,"0",dob,profile_photo))
    connection.commit()



    

def get_user_by_username(connection, username):
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username=?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

def get_user_by_user_id(connection, user_id):
    cursor = connection.cursor()
    query = "SELECT * FROM USERS WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def get_user_with_posts(connection, username):
    user = get_user_by_username(connection, username)

    if user is None:
        return None 

    cursor = connection.cursor()
    query = "SELECT * FROM POSTS WHERE user_id = ?"
    cursor.execute(query, (user[0],))  

    posts = []
    for row in cursor.fetchall():
        post = {
            "post_id": row[0],
            "user_id": row[1],
            "description": row[3],
            "image_data": row[4],
            "image_ext": row[5],
            "date": row[2],
            "username": username, 
        }
        posts.append(post)

    user_with_posts = {
        "user_id": user[0],
        "username": user[1],
        "posts": posts,
    }
    return user_with_posts


# Posts

def init_posts(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS POSTS (
                post_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                image_data TEXT,
                image_ext TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
    """
    )
    connection.commit()

def add_post(connection, user_id, description, image_data, image_ext, date):
    cursor = connection.cursor()
    query = "INSERT INTO POSTS (user_id, description, image_data , image_ext,date) VALUES(?, ?, ?, ?,?)"
    cursor.execute(query, (user_id, description, image_data, image_ext, date))
    connection.commit()

def get_all_posts(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM POSTS"
    cursor.execute(query)
    posts = list()
    for row in cursor.fetchall():
        post = dict()
        post["post_id"] = row[0]
        post["user_id"] = row[1]
        post["description"] = row[3]
        post["image_data"] = row[4]
        post["image_ext"] = row[5]
        post["date"] = row[2]
        user_row = get_user_by_user_id(connection, int(row[1]))
        if user_row:
            post["admin"] = user_row[3]
            post["username"] = user_row[1]
        posts.append(post)
    return posts

def get_all_users(connection):
    cursor = connection.cursor()
    query = "SELECT username FROM users"
    cursor.execute(query)
    users = [row[0] for row in cursor.fetchall()]  # Extract usernames from the result
    return users


def get_post_by_post_id(connection, post_id):
    cursor = connection.cursor()
    query = "SELECT * FROM POSTS WHERE POST_ID = ?"
    cursor.execute(query, (post_id,))
    post = dict()
    for row in cursor.fetchall():
        post["post_id"] = row[0]
        post["user_id"] = row[1]
        post["description"] = row[3]
        post["image_data"] = row[4]
        post["image_ext"] = row[5]
        post["date"] = row[2]
        user_row = get_user_by_user_id(connection, int(row[1]))
        if user_row:
            post["admin"] = user_row[3]
            post["username"] = user_row[1]
    return post

def get_all_userid(connection):
    cursor = connection.cursor()
    query = "SELECT id FROM users"
    cursor.execute(query)
    user_ids = [row[0] for row in cursor.fetchall()]
    return user_ids


def delete_post_by_id(connection, post_id):
    cursor = connection.cursor()
    query = "DELETE FROM POSTS WHERE post_id = ?"
    cursor.execute(query, (post_id,))
    connection.commit()

# Comments

def init_comments(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS COMMENTS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                comment TEXT not null,
                post_id INTEGER NOT NULL,
                date text not null,
                FOREIGN KEY (post_id) REFERENCES POSTS (post_id)
            )
    """
    )
    connection.commit()

def add_comment_to_db(connection, user_id, comment_content, post_id , date):
    cursor = connection.cursor()
    query = "INSERT INTO COMMENTS (user_id, comment, post_id,date) VALUES(?, ?, ?,?)"
    cursor.execute(query, (user_id, comment_content, post_id,date))
    connection.commit()

def get_comments_by_post_id(connection, post_id):
    cursor = connection.cursor()
    # print(post_id)
    query = "SELECT * FROM COMMENTS WHERE post_id = ?"
    cursor.execute(query, (post_id,))
    comments=list()
    for row in cursor.fetchall():
        comment = dict()
        comment["id"] = row[0]
        comment["user_id"] = row[1]
        comment["comment"] = row[2]
        comment["date"] = row[4]
        user_row = get_user_by_user_id(connection, int(row[1]))
        if user_row:
            comment["admin"] = user_row[3]
            comment["username"] = user_row[1]
        comments.append(comment)
    return comments

def delete_comment_by_id(connection, comment_id):
    cursor = connection.cursor()
    query = "DELETE FROM COMMENTS WHERE ID = ?"
    cursor.execute(query, (comment_id,))
    connection.commit()

