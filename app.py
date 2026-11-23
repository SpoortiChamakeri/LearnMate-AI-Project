from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = "foodshare-demo-key"
DB = Path(__file__).with_name("foodshare.db")

def connect():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, donor_name TEXT NOT NULL,
            food_name TEXT NOT NULL, quantity INTEGER NOT NULL, location TEXT NOT NULL,
            pickup_time TEXT NOT NULL, notes TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Available', created_at TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS ngos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, organization_name TEXT NOT NULL,
            contact_person TEXT NOT NULL, email TEXT NOT NULL UNIQUE, location TEXT NOT NULL)""")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        f = {k: request.form.get(k, "").strip() for k in
             ["donor_name","food_name","quantity","location","pickup_time","notes"]}
        if not all(f[k] for k in ["donor_name","food_name","quantity","location","pickup_time"]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("home"))
        try:
            q = int(f["quantity"])
            if q < 1: raise ValueError
        except ValueError:
            flash("Quantity must be a positive whole number.", "error")
            return redirect(url_for("home"))
        with connect() as c:
            c.execute("""INSERT INTO donations
            (donor_name,food_name,quantity,location,pickup_time,notes,created_at)
            VALUES (?,?,?,?,?,?,?)""",
            (f["donor_name"],f["food_name"],q,f["location"],f["pickup_time"],f["notes"],
             datetime.now().isoformat(timespec="minutes")))
        flash("Donation submitted successfully!", "success")
        return redirect(url_for("home"))
    with connect() as c:
        donations = c.execute("SELECT * FROM donations ORDER BY id DESC").fetchall()
    return render_template("index.html", donations=donations)

@app.route("/ngo/register", methods=["GET","POST"])
def ngo_register():
    if request.method == "POST":
        f = {k: request.form.get(k,"").strip() for k in
             ["organization_name","contact_person","email","location"]}
        if not all(f.values()):
            flash("Please complete every field.", "error")
            return redirect(url_for("ngo_register"))
        try:
            with connect() as c:
                c.execute("INSERT INTO ngos (organization_name,contact_person,email,location) VALUES (?,?,?,?)",
                          tuple(f.values()))
            flash("NGO registered successfully.", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("That email is already registered. Use another email.", "error")
    return render_template("ngo_register.html")

@app.route("/ngo/dashboard")
def dashboard():
    with connect() as c:
        ngos = c.execute("SELECT * FROM ngos ORDER BY id DESC").fetchall()
        donations = c.execute("SELECT * FROM donations ORDER BY id DESC").fetchall()
    return render_template("ngo_dashboard.html", ngos=ngos, donations=donations)

@app.route("/donation/<int:donation_id>/claim", methods=["POST"])
def claim(donation_id):
    ngo_id = request.form.get("ngo_id","")
    with connect() as c:
        ngo = c.execute("SELECT id FROM ngos WHERE id=?",(ngo_id,)).fetchone()
        d = c.execute("SELECT id,status FROM donations WHERE id=?",(donation_id,)).fetchone()
        if not ngo or not d:
            flash("Choose a registered NGO and valid donation.", "error")
        elif d["status"] != "Available":
            flash("This donation is already claimed.", "error")
        else:
            c.execute("UPDATE donations SET status='Claimed' WHERE id=?",(donation_id,))
            flash("Donation claimed. Contact the donor to coordinate pickup.", "success")
    return redirect(url_for("dashboard"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/health")
def health():
    return {"status":"ok","app":"FoodShare"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
