from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Recipe:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_thirty_min = bool(data["under_thirty_min"])
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data['user_id']

    @staticmethod
    def validate_recipe(recipe_form):
        is_valid = True 
        errors = []
        #NAME
        if len(recipe_form['name']) < 3:
            errors.append("Name must be at least 3 characters.")
            is_valid = False
        #DESCRIPTION
        if len(recipe_form['description']) < 3 :
            errors.append("Description must be at least 3 characters.")
            is_valid = False
        #INSTRUCTION
        if len(recipe_form['instructions']) < 3:
            errors.append("Instructions must be at least 3 characters.")
            is_valid = False
        return is_valid, errors
    #SAVE RECIPE
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes (name, instructions, description, date_made, under_thirty_min, created_at, updated_at, user_id) VALUES (%(name)s, %(instructions)s, %(description)s, %(date_made)s, %(under_thirty_min)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('db_recipes').query_db( query, data )
    #GET
    @classmethod
    def get(cls, id ):
        query = "SELECT * FROM recipes JOIN users ON user_id = users.id WHERE recipes.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL('db_recipes').query_db(query, data)
        if results:
            instance = cls(results[0])
            instance.user = user.User(results[0])
            return instance
        return None
    
    def delete(self):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {'id': self.id}
        connectToMySQL('db_recipes').query_db(query, data)
        return True
    
    def update(self):
        query = "UPDATE recipes SET name = %(name)s, instructions =  %(instructions)s, description =  %(description)s, date_made =  %(date_made)s, under_thirty_min =  %(under_thirty_min)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'name': self.name,
            'instructions': self.instructions,
            'description': self.description,
            'date_made': self.date_made,
            'under_thirty_min': self.under_thirty_min
        }
        connectToMySQL('db_recipes').query_db( query, data )
        return True
    #GET ALL RECIPES
    @classmethod
    def get_all(cls):

        resultados_instancias = []
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        resultados = connectToMySQL("db_recipes").query_db(query)

        for resultado in resultados:
            instancia = cls(resultado)
            instancia.user = user.User(resultado)
            resultados_instancias.append(instancia)
        return resultados_instancias