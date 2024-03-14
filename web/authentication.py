from flask import Blueprint, render_template, request
import logging

auth = Blueprint("authentication", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'GET':
            return render_template("login.html")
      elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            return render_template("loginResult.html", username=username)

@auth.route('/register', methods=['GET', 'POST'])
def register():
      if request.method == 'GET':
            return render_template("register.html")
      elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            return render_template("registerResult.html", username=username)