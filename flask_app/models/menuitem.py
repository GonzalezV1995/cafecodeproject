from ast import If
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class menuitem:
    db = "cafecode"
    def __init__(self, menu_item):
        self.id = menu_item['user_id']
        self.smallbyte = menu_item['smallbyte']
        self.mediumbyte = menu_item['mediumbyte']
        self.largebyte = menu_item['largebyte']
        self.steampunklatte = menu_item['steampunklatte']
        self.redespresso = menu_item['redespresso']
        self.bubbletea = menu_item['bubbletea']
        self.salmonpoke = menu_item['salmonpoke']
        self.ramen = menu_item['ramen']
        self.bahnmi = menu_item['bahnmi']
        self.created_at = menu_item['created_at']
        self.updated_at = menu_item['updated_at']

        # do user_sighting instead of data
    
    def __repr__(self) -> str:
        return f'user: {self.first_name} {self.last_name}'
        # what does this do again?


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(address)s, %(city)s, %(state)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)
