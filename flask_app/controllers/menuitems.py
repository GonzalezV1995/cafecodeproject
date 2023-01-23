from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.menuitem import menuitem
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


