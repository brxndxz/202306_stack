from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Painting:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.price = data["price"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
    @staticmethod
    def validate_painting(painting_form):
        is_valid = True 
        errors = []
        #TITLE
        if len(painting_form['title']) < 2:
            errors.append("Title must be at least 2 characters.")
            is_valid = False
     
        #DESCRIPTION
        if len(painting_form['description']) < 10 :
            errors.append("Description must be at least 10 characters.")
            is_valid = False
        #PRICE
        if float(painting_form['price']) <= 0:
            errors.append("Price should be greater than 0")
        return is_valid, errors
        
    #SAVE
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO paintings (title, description, price, created_at, updated_at, user_id) VALUES (%(title)s, %(description)s, %(price)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('db_paintings').query_db( query, data )
    
    @classmethod
    def get_all(cls):
        results_instances = []
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL("db_paintings").query_db(query)

        for result in results:
            instance = cls(result)
            instance.user = user.User(result)
            results_instances.append(instance)
        return results_instances
    
    @classmethod
    def get(cls, id ):

        query="SELECT * FROM paintings JOIN users ON user_id = users.id WHERE paintings.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL('db_paintings').query_db(query, data)

        if results:
            instance = cls(results[0])
            instance.user = user.User(results[0])
            return instance
        return None
    
    def delete(self):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        data = {'id': self.id}
        connectToMySQL('db_paintings').query_db(query, data)
        return True
    
    def update(self):
        query = "UPDATE paintings SET title = %(title)s, description =  %(description)s, price =  %(price)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price
        }
        connectToMySQL('db_paintings').query_db( query, data )
        return True