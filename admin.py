from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from supabase_client import supabase
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session["admin"] = True
            return redirect("/admin")
        return "Invalid login"
    return render_template("login.html")

@app.route("/admin")
def dashboard():
    if not session.get("admin"): return redirect("/admin/login")
    members = supabase.table("members").select("*").execute().data
    return render_template("dashboard.html", members=members)

@app.route("/admin/add-member", methods=["POST"])
def add_member():
    if not session.get("admin"): return "Unauthorized", 403
    data = request.form
    supabase.table("members").insert({
        "name": data["name"],
        "phone_number": data["phone"]
    }).execute()
    return redirect("/admin")

@app.route("/admin/add-payment", methods=["POST"])
def add_payment():
    if not session.get("admin"): return "Unauthorized", 403
    data = request.form
    supabase.table("payments").insert({
        "member_id": data["member_id"],
        "amount_due": float(data["amount"]),
        "due_date": data["due_date"]
    }).execute()
    return redirect("/admin")