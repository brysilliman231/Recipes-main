from flask_app import app
from flask import render_template, session, redirect, request, flash 
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.controllers import home
from flask_app.controllers import users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create')
def create():
    print(session['user_id'])
    data = {
        "id" : session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template('create_recipe.html', user = logged_user)

@app.route('/add/recipe', methods=["POST"])
def add_recipe():
    if not session['user_id']:
        return redirect('/')
    data = {
        "name": request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date_made" : request.form['date_made'],
        "under_30" : request.form['under_30'],
        "user_id" : session['user_id']
    }
    new_recipe = Recipe.save(data)
    print(new_recipe)
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    data = {
        "id": id
    }
    recipe = Recipe.get_by_id(data)
    return render_template('view_recipe.html', recipe = recipe)

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {"id": id}
    recipe = Recipe.get_by_id(data)
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": request.form['under_30'],
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id': id}
    Recipe.delete(data)
    return redirect('/dashboard')