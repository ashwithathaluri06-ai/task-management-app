from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# App configuration
app.config["SECRET_KEY"] = "task-management-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User database model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Task database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# Load logged-in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create database tables
with app.app_context():
    db.create_all()


# Home page
@app.route("/")
@login_required
def home():
    return render_template("index.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            return "Username and password are required."

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists."

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("home"))

        return "Invalid username or password."

    return render_template("login.html")


# Logout
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# GET - Read user's tasks
@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return jsonify([
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ])


# POST - Create a new task
@app.route("/api/tasks", methods=["POST"])
@login_required
def create_task():

    data = request.get_json()

    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = Task(
        title=title,
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    }), 201


# PUT - Update task
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    data = request.get_json()

    if "title" in data:
        title = data.get("title", "").strip()

        if not title:
            return jsonify({
                "error": "Task title cannot be empty"
            }), 400

        task.title = title


        if "completed" in data:
            task.completed = data["completed"]

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    })


# DELETE - Delete task
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    })


# Start application
if __name__ == "__main__":
    app.run(debug=True)