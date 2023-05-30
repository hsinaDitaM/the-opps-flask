import json
from flask import (
    Flask,
    redirect,
    render_template,
    request,
)

from database import use_database
from cookie import create_access_token, get_token_payload
from utils import redirect_if_logged_in, admin_only

# number of days until token expires
TOKEN_DURATION = 1

app = Flask(__name__)

@app.route("/")
@redirect_if_logged_in("/dashboard")
def home():
    response = redirect("/login")
    response.delete_cookie("token")
    return response
    
@app.route("/login")
@redirect_if_logged_in("/dashboard")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
@use_database("database.db")
def dashboard_page(database):
    print(request.cookies.get("token"))
    username = get_token_payload(request.cookies.get("token"))["username"]
    user = database.get_user(username)
    return render_template("home.html", user=user)

@app.route("/dashboard/users")
@use_database("database.db")
def users_page(database):
    username = get_token_payload(request.cookies.get("token"))["username"]
    user = database.get_user(username)
    return render_template("users.html", user=user)

@app.route("/api/login", methods=["POST"])
@use_database("database.db")
def login_handler(database):
    try:
        data = request.get_json()
        username, password = data["username"], data["password"]
    except KeyError:
        return json.dumps({
            "status": "error",
            "message": "Missing fields",
        })

    if not all([username, password]):
        return json.dumps({
            "status": "error",
            "message": "Missing fields",
        })
    
    if database.verify_password(username, password):
        token = create_access_token({"username": username}, TOKEN_DURATION)
        response = redirect("/dashboard")
        response.set_cookie("token", token, path="/")
        response.set_data(json.dumps({
            "status": "success",
            "message": "Logged in",
        }))

        return response

    return json.dumps({
        "status": "error",
        "message": "Incorrect username or password",
    })

@app.route("/api/register", methods=["POST"])
@use_database("database.db")
def register_handler(database):
    try: 
        data = request.get_json()
        email, username, password = data["email"], data["username"], data["password"]
    except KeyError:
        return json.dumps({
            "status": "error",
            "message": "Missing fields",
        })

    if not all([email, username, password]):
        return json.dumps({
            "status": "error",
            "message": "Missing fields",
        })
    # check if user exists
    if database.get_user(username) is None:
        database.register_user(email, username, password, "user")

        return json.dumps({
            "status": "success",
            "message": "User registered",
        })

    return json.dumps({
        "status": "error",
        "message": "User already exists",
    })

@app.route("/api/logout", methods=["POST"])
def logout_handler():
    response = redirect("/login")
    response.delete_cookie("token")
    response.set_data(json.dumps({
        "status": "success",
        "message": "Logged out",
    }))

    return response

@app.route("/api/users", methods=["GET"])
@use_database("database.db")
@admin_only()
def get_users(database, admin_user):
    users = database.get_all_users()
    users = map(lambda user: {
        "id": user[0],
        "email": user[1],
        "username": user[2],
        "password": user[3],
        "role": user[4],
    }, users)

    return json.dumps({
        "status": "success",
        "users": list(users),
    })

@app.route("/api/users", methods=["UPDATE"])
@use_database("database.db")
@admin_only()
def update_users(database, admin_user):
    try:
        data = request.get_json()
        user_id, email, username, password, role = data["id"], data["email"], data["username"], data["password"], data["role"]
    except KeyError:
        return json.dumps({
            "status": "error",
            "message": "Missing fields",
        })
    
    success = database.update_user(
        user_id,
        email, 
        username, 
        password, 
        role
    )

    if success:
        return json.dumps({
            "status": "success",
        })

    return json.dumps({
        "status": "error",
        "message": "Unable to update user. Please check console.",
    })

@app.route("/api/users", methods=["DELETE"])
@use_database("database.db")
@admin_only()
def delete_users(database, admin_user):
    try:
        data = request.get_json()
        user_id = data["id"]
    except KeyError:
        return json.dumps({
            "status": "error",
            "message": "Missing fields",
        })
    
    success = database.delete_user(user_id)
    if success:
        return json.dumps({
            "status": "success",
        })

    return json.dumps({
        "status": "Error",
        "message": "Unable to delete user. Please check console.",
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4523, debug=True)