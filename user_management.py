import sqlite3 as sql
import time
import random
import bcrypt


# Inserts user info into database
def insertUser(username, password, DoB):  # hash password and salt and hash
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth,salt) VALUES (?,?,?,?)",
        (username, hash, DoB, salt),
    )
    con.commit()
    con.close()


# Get salt from user
def retrieveSalt(username):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT salt FROM users WHERE username = (?)", (username,))
    return cur.fetchone()[0]


# Create a function to hash and salt the users input to validate, hash pass using salt and given input pass
def hashPass(password, salt):
    pw = password.encode()
    salt = bcrypt.salt()
    hash = bcrypt.hashpw(pw, salt)
    result = bcrypt.checkpw(hash, salt)
    return hash


# Retrieve user info, validate user
def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = (?)", (username,))
    if cur.fetchone() == None:  # checks for a match --> no match (none)
        con.close()
        return False
    else:
        salt = retrieveSalt(username)
        print(salt)
        hashpw = hashPass(salt, password)
        print(hashpw)
        # valid username continued, make a get salt function
        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True

    # if result == password:
    # return True
    hashpw = getHashedPass(salt, password)


# print(result)


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()


# call retrieved users function using hash password

retrieveUsers("hello", "password")

# hashSalt("hello")
