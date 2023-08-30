from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_user(user_form):
        is_valid = True 
        errors = []
        #FIRST NAME
        if len(user_form['first_name']) < 2:
            errors.append("Name must be at least 2 characters.")
            is_valid = False
        if not user_form['first_name'].isalpha():
            errors.append("First name must be only alphabetic characters")
            is_valid = False
        #LAST NAME
        if len(user_form['last_name']) < 2 :
            errors.append("Last name must be at least 2 characters.")
            is_valid = False
        if not user_form['last_name'].isalpha():
            errors.append("Last name must be only alphabetic characters")
            is_valid = False
        #EMAIL
        if not EMAIL_REGEX.match(user_form['email']): 
            errors.append("Invalid email address!")
            is_valid = False
        #PASSWORD
        if len(user_form['password']) < 8:
            errors.append("Password must be at least 8 characters.")
            is_valid = False
        return is_valid, errors
    
    @classmethod 
    def save(cls, result ):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('db_user').query_db( query, result )
    
    @classmethod
    def get_by_email(cls, data: dict):

        query = """SELECT * FROM users WHERE email = %(email)s;"""
        result = connectToMySQL('db_user').query_db(query, data)
        
        if result:
            return cls(result[0])
        return None