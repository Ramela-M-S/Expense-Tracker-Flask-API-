from eta import app,db,login_manager
from flask import render_template,redirect,url_for,flash, request, session
from eta.models import User,Expense
from eta.forms import RegistrationForm
from flask_login import login_user,logout_user,current_user,login_required
import requests
from eta import resource


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#HOME PAGE
@app.route("/")
def home_page():
    return render_template("home.html")


#REGISTER PAGE
@app.route("/register", methods = ["GET", "POST"])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user:
            flash("Welcome Back! You had already registered!","danger")
            return redirect(url_for("login_page"))
        u1 = User(name = form.username.data,
                  email = form.email.data)
        u1.set_password(form.password.data)
        db.session.add(u1)
        db.session.commit()
        flash("Account Created Successfully! Please Log In")
        return redirect(url_for("login_page"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", "danger")
    return render_template("register.html", form = form)
        
        
#LOGIN PAGE
@app.route("/login", methods = ["GET","POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email = email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Successfully LoggedIn", "success")
            return redirect(url_for("dashboard_page"))
        else:
            flash("Login Failed, Check Email Id and Password","danger")
    return render_template("login.html")



#DASHBOARD PAGE
@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

#SHOW EXPENSE PAGE
@app.route("/s_expense")
@login_required
def show_expense_page():
    url=f"http://localhost:5000/api/expenses/{current_user.id}"
    response = requests.get(url)
    expenses = response.json()
    return render_template("show_expense.html", expenses=expenses)



#ADD EXPENSE PAGE
@app.route("/a_expense", methods=["GET","POST"])
@login_required
def add_expense_page():
    url = f"http://localhost:5000/api/a_expenses/{current_user.id}"
    if request.method == "POST":
        data = {"title":request.form["title"],
                "amount":request.form["amount"],
                "category":request.form["category"],
                "date":request.form["date"],
                }
        requests.post(url, json = data)
        return redirect(url_for("show_expense_page"))
    return render_template("add_expense.html")

#DELETE EXPENSE PAGE
@app.route("/delete_expense/<int:id>")
def delete_expense(id): 
    requests.delete(f"http://127.0.0.1:5000/api/delete/{id}")
    return redirect(url_for("show_expense_page"))
    


#MONTHLY EXPENSE PAGE
@app.route("/monthly", methods=["GET", "POST"])
@login_required
def monthly_page():
    total_data = None
    if request.method == "POST":
        month = request.form.get("month")  
        url = f"http://127.0.0.1:5000/api/monthly/{month}/{current_user.id}"
        res = requests.get(url)
        total_data = res.json()  
    return render_template("monthly.html", total_data=total_data)







#LOGOUT PAGE
@app.route("/logout")
def logout_page():
    logout_user()
    flash("Logged Out Successfully!","success")
    return redirect(url_for("home_page"))
        



























