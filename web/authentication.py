from flask import Blueprint, render_template, request, session
import logging
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint("authentication", __name__)

# Define la ruta para que los usuarios inicien sesión
@auth.route('/login', methods=['GET', 'POST'])
def login():
      user = session.get('user')
      if request.method == 'GET':
            return render_template("login.html", user = user)
      elif request.method == 'POST':
            usern = request.form['username']
            passw = request.form['password']
            userDB = db.session.query(User).filter_by(username=usern).first()
            if not userDB:
                  return render_template("badlogin.html")
            else:
                  if check_password_hash(userDB.password, passw):
                        session['user'] = usern
                        return render_template("loginResult.html", username=usern)
                  else:
                       return render_template("badlogin.html") 

# Define la ruta para que los usuarios se registren
@auth.route('/register', methods=['GET', 'POST'])
def register():
      if request.method == 'GET':
            return render_template("register.html")
      elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            if not db.session.query(User).filter_by(username=username).first():
                  new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
                  db.session.add(new_user)
                  db.session.commit()
            else:
                  return render_template("register.html")
            return render_template("registerResult.html", username=username)

@auth.route('/logout')
def logout():
      session.pop('user', None)
      return render_template("logout.html")