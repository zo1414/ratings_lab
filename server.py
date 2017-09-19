"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify,render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1,3])
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_form():

    pass

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Check db for email."""

    input_email = request.form.get("email")
    input_password = request.form.get("password")

    if not User.query.filter(User.email == input_email).all():

        new_user = User(email=input_email, password=input_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Successfully registered")

    else:
        flash("User already registered")

    #session["user"] = [input_email, input_password]
    # print "added to session %s %s" % (input_email, input_password)
    return redirect("/")

@app.route("/login", methods=["GET"])
def login_form():

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login_process():
    """log user into session"""

    input_email = request.form.get("email")
    input_password = request.form.get("password")

    current_user = User.query.filter(User.email == input_email).first()

    if "user" in session:
        flash("%s is logged in." % (session["user"]))
        return redirect("/")

    if current_user is not None and current_user.password == input_password:
        session["user"] = input_email
        flash("Logged In")
        return redirect("/")
    else:
        flash("Login failed")
        return redirect("/login")

@app.route("/logout")
def logout_process():
    """Logs user out by removing info from session."""

    session.pop("user")
    flash("Logged out")
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
