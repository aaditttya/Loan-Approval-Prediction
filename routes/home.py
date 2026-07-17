from flask import Blueprint, render_template


home_bp = Blueprint(
    "home",
    __name__
)


@home_bp.route("/")
def index():
    """
    Display the main loan prediction page.
    """

    return render_template(
        "index.html"
    )