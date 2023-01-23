from ast import If
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db = "cafecode"
    def __init__(self, user_account):
        self.id = user_account['id']
        self.first_name = user_account['first_name']
        self.last_name = user_account['last_name']
        self.email = user_account['email']
        self.address=user_account['address']
        self.city = user_account['city']
        self.state = user_account['state']
        self.password = user_account['password']
        self.created_at = user_account['created_at']
        self.updated_at = user_account['updated_at']

        # do user_sighting instead of data
    
    def __repr__(self) -> str:
        return f'user: {self.first_name} {self.last_name}'
        # what does this do again?

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email, address, city, state, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(address)s, %(city)s, %(state)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

        # this method allows for the user to input a row of data into the database. Need to connect to request.form in route 


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    # get all what? get_all_users
        # create a method for validating user. Username and passwords must match the database and be the correct number of characters. 
        # password has to also match the confirm password box in the database
    
    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(user["email"]) <= 0:
            is_valid = False
            flash("Email is required.")
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        elif results:
            flash("Email address is already taken.")
            is_valid = False

        if len(user['first_name']) < 2:
            flash("First name has to be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name has to be at least 2 characters")
            is_valid = False
        if len(user['address']) < 2:
            flash("Address has to be at least 8 characters")
            is_valid = False

        if len(user['city']) < 2:
            flash("City has to be at least 4 characters")
            is_valid = False

        if len(user['State']) < 2:
            flash("State has to be at least 2 characters")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password has to be at least 8 characters")
            is_valid = False
        if user['confirm_password']!=user['password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_log(data):
        is_valid = True
        #  we have to match the user email input to the list of emails in the database. There cannot be match or else their email will be taken
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,data)
        if not results:
            is_valid = False
            flash("Account is not registered.")
        elif not bcrypt.check_password_hash(User(results[0]).password, data['password']):
            #we need to idenitfy the password in the database to match it with the password inputted into the form. User(results[0]) is us looking for the password in the database 
            print("email",User(results[0]))
            print('invalid password')
            flash("Invalid Email or Password")
            is_valid = False

        return is_valid

        # return is_valid=going to return true if it passed all the checks
        # returns id, first name, and last name, otherwise none- nothing will be returned to the database--- validation failed


    @classmethod
    def get_user_by_id(cls,data):
        query="SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        #Check to see if there were any results, if not, the id does not exist in the db
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user

# return instance of a user. Session just saves the id

    @classmethod
    def get_user_by_email(cls,data):
        query="SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        #Check to see if there were any results, if not, the email does not exist in the db
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user



    
