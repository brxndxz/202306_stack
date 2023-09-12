from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

#SHOW

@app.route("/recipes")
def show_recipes():

    recipes = Recipe.get_all()
    print(recipes)

    if "user" not in session:
        flash('You need to log in', 'error')
        return redirect("/")
    user_session=User.get_id(session["user"])
    return render_template("show_recipes.html", recipes = recipes, user_session = user_session)

#SHOW FORM CREATE 

@app.route("/recipes/new")
def create_recipes():
    if "user" not in session:
        flash('You need to log in', 'error')
        return redirect("/")
    return render_template("new_recipe.html")

#PROCESS CREATE 

@app.route('/recipes/create', methods=['POST'])
def process_create_recipe():
    name = request.form["name"]
    under_thirty_min = request.form["under_thirty_min"]
    instructions = request.form["instructions"]
    description = request.form["description"]
    date_made = request.form["date_made"]
    user_id = session['user']
    
    is_valid, errors = Recipe.validate_recipe(request.form)

    if not is_valid:
        for error in errors:
            print("ERROR: ", error)
            flash(error, "error")
        return redirect('/recipes/new')

    data = Recipe.save({
        "name": name,
        "under_thirty_min": under_thirty_min,
        "instructions": instructions,
        "description": description,
        "date_made": date_made,
        "user_id": user_id
    })
    
    if data:
        flash("Your recipe was added succesfully.", "success")
    else:
        flash("Error, failed adding your recipe.", "error")
    return redirect("/recipes")

#DELETE 
@app.route("/recipes/<id>/delete")
def delete(id):

    delete_recipe = Recipe.get(id)
    delete_recipe.delete()

    flash("Recipe deleted", "success")
    return redirect("/recipes")

#EDIT 

@app.route("/recipes/<id>/edit")
def edit_(id):
    
    if "user" not in session:
        flash('You need to log in', 'error')
        return redirect("/")
    
    recipe = Recipe.get(id)

    return render_template("edit_recipe.html", recipe = recipe)

#PROCESS EDIT 

@app.route("/recipes/process_edit/<id>", methods=['POST'])
def process_edit_recipe(id):
    recipe = Recipe.get(id)
    recipe.name = request.form['name']
    recipe.under_thirty_min = request.form['under_thirty_min']
    recipe.instructions = request.form['instructions']
    recipe.description = request.form['description']
    recipe.date_made = request.form['date_made']
    is_valid, errors = Recipe.validate_recipe(request.form)
    
    if not is_valid:
        for error in errors:
            print("ERROR: ", error)
            flash(error, "error")
        return redirect('/recipes/{}/edit'.format(id))
    
    recipe.update()

    return redirect("/recipes")

#SHOW
@app.route("/recipes/<id>")
def show_recipe(id):

    if "user" not in session:
        flash('You need to log in', 'error')
        return redirect("/")

    user_session=User.get_id(session["user"])
    
    recipe = Recipe.get(id)

    return render_template("show_a_recipe.html", recipe=recipe, user_session=user_session)