from flask import Flask,flash,render_template,request,session,redirect,url_for,g
from flask_hashing import Hashing
from sqlalchemy import create_engine

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/blog")
def lblog():
    return render_template("blog.html")

if __name__ == "__main__":
    app.run()
    