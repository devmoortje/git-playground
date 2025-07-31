from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash

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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        # A hash is the result of a hash function that outputs a seemingly random string for an input
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Remember user name
        session["user_name"] = rows[0]["username"]

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
            return apology("must provide username", 400)
                
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash('Username already taken')
            return redirect('/register')

        if not password:
            flash("Must provide password")
            return redirect("/register")

        if not confirmation:
            flash("Must provide password confirmation")
            return redirect("/register")

        if password != confirmation:
            flash("Password and confirmation must match")
            return redirect("/register")

        # Create new user

        # Instantiate a User class object to be written to db
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )

        
        db.session.add(new_user)
        db.session.commit()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")
