from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
from flask_app.controllers import recipes
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipes_schema').query_db(query,data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"
        results =  connectToMySQL('recipes_schema').query_db(query,data)
        user = cls(results[0])
        for row in results: 
            recipe_data = {
                "id" : row["recipes.id"],
                "name": row["name"],
                "description" : row["description"],
                "instructions" : row["instructions"],
                "under_30" : row["under_30"],
                "date_made" : row["date_made"],
                "created_at" : row["created_at"],
                "updated_at" : row["updated_at"],
                "user_id" : row["user_id"]
            }
            user.recipes.append(recipe.Recipe(recipe_data))
        print(user.recipes)
        return user
    
    @classmethod
    def get_user_by_id(cls, data): 
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])
    
    @staticmethod
    def validate_user_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be greater than 8 characters long.')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters long.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be greater than 8 characters long")
        return is_valid
    
    