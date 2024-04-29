"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()


@app.route("/")
def show_home():
    return redirect("/users")


@app.route("/users")
def show_user_list():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def show_new():
    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Allows user to submit information to be added to db."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    img_url = img_url if img_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def post_edit(user_id):
    """Allows user to edit user information on db."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["img_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user from db."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user profile page."""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show user post form."""
    user = User.query.get_or_404(user_id)
    return render_template("post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def post_story(user_id):
    """Posts user story to the database."""
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(user_id=user.id, title=title, content=content)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/posts/{new_post.id}")


@app.route("/posts/<int:post_id>")
def show_story(post_id):
    """Shows user post."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("post_details.html", post=post, user=user)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_story(post_id):
    """Deletes user story from the database."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Shows user the form to edit a previous post."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("edit_post.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Allows user to edit the post in the database."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")
