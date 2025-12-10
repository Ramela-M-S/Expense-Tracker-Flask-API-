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
@login_required
def dashboard_page():
    return render_template("dashboard.html")

#SHOW EXPENSE PAGE
@app.route("/s_expense")
@login_required
def show_expense_page():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template("show_expense.html", expenses=expenses)

#ADD EXPENSE PAGE
@app.route("/a_expense", methods=["GET","POST"])
@login_required
def add_expense_page():
    if request.method == "POST":
        title = request.form.get("title")
        amount = float(request.form.get("amount", 0))
        category = request.form.get("category")
        date = request.form.get("date")

        if not title or not category or not date:
            flash("Please fill all fields!", "danger")
            return redirect(url_for("add_expense_page"))

        new_expense = Expense(
            title=title,
            amount=amount,
            category=category,
            date=date,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added successfully!", "success")
        return redirect(url_for("show_expense_page"))

    return render_template("add_expense.html")

#DELETE EXPENSE PAGE
@app.route("/delete_expense/<int:id>")
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash("Not authorized to delete this expense!", "danger")
        return redirect(url_for("show_expense_page"))
    
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("show_expense_page"))
  


#MONTHLY EXPENSE PAGE
@app.route("/monthly", methods=["GET", "POST"])
@login_required
def monthly_page():
    total_data = None
    if request.method == "POST":
        month = request.form.get("month")  # e.g., "04" for April
        expenses = Expense.query.filter_by(user_id=current_user.id).all()
        total = sum(exp.amount for exp in expenses if exp.date[5:7] == month)
        total_data = {"Month": month, "Total_Spent": total}
    return render_template("monthly.html", total_data=total_data)






#LOGOUT PAGE
@app.route("/logout")
def logout_page():
    logout_user()
    flash("Logged Out Successfully!","success")
    return redirect(url_for("home_page"))
        



























