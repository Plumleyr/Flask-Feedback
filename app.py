from flask import Flask, redirect, render_template, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///hashing_logging"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "Secret"

connect_db(app)

@app.route("/")
def go_to_register():
    return redirect("/register")

@app.route("/register", methods = ["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.firstname.data
        last_name = form.lastname.data

        new_user = User.register(name, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["user_username"] = new_user.username

        return redirect(f"/users/{new_user.username}")
    
    return render_template("register.html", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        user = User.authenticate(name, password)
        
        if user:
            session["user_username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Wrong Username / Password"]

    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    session.pop("user_username")
    return redirect("/login")

@app.route("/users/<username>")
def profile(username):

    if 'user_username' not in session:
        flash("Please login first!", "danger")
        return redirect("/login")
    
    user = User.query.get_or_404(username)
    feedbacks = user.feedbacks

    return render_template("profile.html", user = user, feedbacks = feedbacks)

@app.route("/users/<username>/delete", methods = ["POST"])
def delete_user(username):

    if 'user_username' not in session:
        flash("Please login first!", "danger")
        return redirect("/login")
    
    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()

    return redirect("/register")

@app.route("/users/<username>/feedback/add", methods = ["GET", "POST"])
def feedback(username):
    
    if 'user_username' not in session:
        flash("Please login first!", "danger")
        return redirect("/login")

    form = FeedbackForm()

    user = User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title = title, content = content, user = user)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"/users/{user.username}")

    return render_template("feedback.html", form = form)

@app.route("/feedback/<feedback_id>/update", methods = ["GET", "POST"])
def update_feedback(feedback_id):
    
    if 'user_username' not in session:
        flash("Please login first!", "danger")
        return redirect("/login")

    feedback = Feedback.query.get_or_404(feedback_id)

    form = FeedbackForm(obj = feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.user.username}")

    return render_template("update_feedback.html", form = form)

@app.route("/feedback/<feedback_id>/delete", methods = ["POST"])
def delete_feedback(feedback_id):

    if 'user_username' not in session:
        flash("Please login first!", "danger")
        return redirect("/login")
    
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{user.username}")