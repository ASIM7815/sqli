from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.models import get_user_by_username, get_ordinary_records, get_ordinary_record_by_id, search_ordinary_records_safe

bp = Blueprint("main", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_user_by_username(username)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid credentials", "error")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", username=session.get("username"))


@bp.route("/records")
def records():
    records = get_ordinary_records()
    return render_template("records.html", records=records)


@bp.route("/records/<int:rec_id>")
def record_detail(rec_id):
    record = get_ordinary_record_by_id(rec_id)
    if not record:
        return render_template("404.html"), 404
    return render_template("record_detail.html", record=record)