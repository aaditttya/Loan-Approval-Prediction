from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import check_password_hash

from database import get_admin_by_username


auth_bp = Blueprint(
    "auth",
    __name__
)


def login_required(route_function):
    """
    Protect routes that require admin login.
    """

    @wraps(route_function)
    def wrapped_route(*args, **kwargs):

        if not session.get("admin_logged_in"):

            return redirect(
                url_for("auth.login")
            )

        return route_function(
            *args,
            **kwargs
        )

    return wrapped_route


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():
    """
    Admin login page and authentication.
    """

    if session.get("admin_logged_in"):

        return redirect(
            url_for("history")
        )

    error_message = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not username or not password:

            error_message = (
                "Please enter username and password."
            )

        else:

            admin = get_admin_by_username(
                username
            )

            if (
                admin is not None
                and check_password_hash(
                    admin["password_hash"],
                    password
                )
            ):

                session.clear()

                session[
                    "admin_logged_in"
                ] = True

                session[
                    "admin_username"
                ] = admin["username"]

                return redirect(
                    url_for("history")
                )

            error_message = (
                "Invalid username or password."
            )

    return render_template(
        "login.html",
        error_message=error_message
    )


@auth_bp.route("/logout")
def logout():
    """
    End admin session.
    """

    session.clear()

    return redirect(
        url_for("auth.login")
    )