from functools import wraps

import json
from flask import request, redirect
from cookie import cookie_token_isvalid

from cookie import get_token_payload

def redirect_if_logged_in(location):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if cookie_token_isvalid(request.cookies):
                return redirect(location)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_only():
    def decorator(f):
        @wraps(f)
        def decorated_function(database, *args, **kwargs):
            username = get_token_payload(request.cookies.get("token"))["username"]
            user = database.get_user(username)
            if user[4] == "admin":
                return f(database, user, *args, **kwargs)
            return json.dumps({
                "status": "error",
                "message": "Unauthorized",
            })
        return decorated_function
    return decorator