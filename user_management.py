import sqlite3 as sql
import time
import random
import bcrypt


def insertUser(username, password, DoB): #hash password and salt and hash
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt) 
    
    cur.execute(  "INSERT INTO users (username,password,dateOfBirth,salt) VALUES (?,?,?,?)",
    (username, hash, DoB,salt), )
    con.commit()
    con.close()
    


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    result=cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    
    print(result.fetchone())
    #fetch one returns the first row 
    #validate user sign in 
    if password == '{hash}': 
        return True
    #write the code to now check the two hash values with bcrypt using the saved salt
    #get the password
    
    if cur.fetchone() == None:
        con.close()
        return False
    else:   
        
        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        result = cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        print(username,password)
        print(result.fetchone())
        
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True




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
