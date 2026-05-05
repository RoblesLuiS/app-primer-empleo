from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


app.secret_key = "secretkey"

def get_db():
    conn = sqlite3.connect("empleos.db")
    conn.row_factory = sqlite3.Row
    return conn



def home():
    db = get_db()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    return render_template("home.html", jobs=jobs)



def job_detail(id):
    db = get_db()
    job = db.execute("SELECT * FROM jobs WHERE id=?", (id,)).fetchone()
    return render_template("job_detail.html", job=job)



def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute("INSERT INTO users (username,password) VALUES (?,?)",
                   (username, password))
        db.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)).fetchone()

        if user:
            session["user"] = username
            return redirect(url_for("home"))

    return render_template("login.html")



def apply(job_id):

    if "user" not in session:
        return redirect(url_for("login"))

    db = get_db()
    db.execute("INSERT INTO applications (username,job_id) VALUES (?,?)",
               (session["user"], job_id))
    db.commit()

    return redirect(url_for("home"))



def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)