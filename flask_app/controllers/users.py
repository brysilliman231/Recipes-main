from flask_app import app
from flask import render_template, session, redirect, request, flash 
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.controllers import home
from flask_app.controllers import recipes
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=["POST"])
def register():
    if User.get_by_email(request.form):
        flash("This email address is already in use.")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    if not bcrypt.check_password_hash(pw_hash, request.form['confirm_password']):
        flash('Invalid Email and/or Password')
        print('this will be an invalid password')
        return redirect('/')
    data = {
        "first_name" : request.form["first_name"], 
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash,
        "confirm_password" : request.form['confirm_password']
    }
    if not User.validate_user(data):
        return redirect('/')
    user_id = User.save(data)
    session['user_id'] = user_id
    print("you made it here!")
    return redirect('/dashboard')

@app.route('/logout', methods=["POST"])
def logout():
    print('this is session before', session)
    session.clear()
    print('this is session after', session)
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    data = {
        "email" : request.form['email'],
        "password" : request.form['password']
    }
    if not User.validate_user_login(data):
        return redirect('/')
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email and/or Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email and/or Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')