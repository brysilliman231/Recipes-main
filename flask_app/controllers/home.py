from flask_app import app
from flask import render_template, session, redirect, request, flash 
from flask_app.models.recipe import Recipe
from flask_app.controllers import users
from flask_app.controllers import recipes
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if session.get('user_id'):
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    logged_user = User.get_by_id(data)
    # user_recipes = Recipe.get_by_id(data)
    return render_template('dashboard.html', user = logged_user)