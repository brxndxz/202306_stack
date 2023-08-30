from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def show_index():
    return render_template("index.html")

@app.route("/home")
def show_home():
    if "user" not in session:
        return redirect("/index")
    return render_template("home.html")

@app.route('/register/user', methods=['POST'])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords don't match", "warning")
        return redirect('/')
    
    is_valid, errors = User.validate_user(request.form)

    if not is_valid:
        print("NO PASA LA VALIDACION", errors)
        for error in errors:
            print("ERROR: ", error)
            flash(error, "error")
        return redirect('/')

    password_hash = bcrypt.generate_password_hash(password)
    print(password_hash)

    result = User.save({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password_hash
    })
    
    if result:
        flash("Registered Successfully.", "success")
    else:
        flash("Error.", "error")
    return redirect("/")

@app.route("/login/", methods=["POST"])
def login():
   
    email = request.form["email"]
    password = request.form["password"]

    data = {"email": email}
    user = User.get_by_email(data)

    if not user:
        flash("User or password is incorrect", "error")
        return redirect("/")

    check_password = bcrypt.check_password_hash(user.password, password)
    if check_password:
        session["user"] = {
            "id": user.id,
            "email": user.email
        }
        flash("You are logged in", "info")
    else:
        flash("Error", "error")
        return redirect('/')

    return redirect('/home')
@app.route("/logout/")
def logout():
    
    if "user" not in session:
        return redirect('/')

    session.clear()
    flash("You logged out", "info")
    return redirect('/')