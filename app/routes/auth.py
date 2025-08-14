from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from app import db
from helpers import apology, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST f(as by submitting a form via POST)
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Ensure username was submitted
        if not username:
            return "Please enter username", 400
        
        # Ensure password was submitted
        if not password:
            return "Please enter password", 400

        # Query database for username
        # User is sqlalchemy model representing users table
        user = User.query.filter_by(username=username).first()

        # Ensure username was submitted
        if not user:
            return "Invalid id", 400
        
        # Ensure correct password was submitted
        if not check_password_hash(user.password_hash, password):
            return "Invalid password", 400

        # Set user_id session
        session["user_id"] = user.id

        # Set user_name session
        session["user_name"] = user.username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Ensure username was submitted
        if not username:
            return "Please enter username", 400
   
        # Ensure password was submitted
        if not password:
            return "Please enter password", 400
        
        # Ensure confirmation was submitted
        if not confirmation:
            return "Please enter confirmation", 400
        
        # Ensure password and comfirmation match
        if password != confirmation:
            return "Please match password and password confirmation", 400

        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash('Username already taken')
            return redirect('/register')



        # Create new user

        # Instantiate a User class object to be written to db
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )


        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully!')
        return redirect('/login')

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")
