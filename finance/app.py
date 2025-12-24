import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """عرض المحفظة الاستثمارية"""
    stocks = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    total_value = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["total_shares"]
        total_value += stock["total"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value)


@app.route("/register", methods=["GET", "POST"])
def register():
    """تسجيل مستخدم جديد"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must provide username and password")

        if password != confirmation:
            return apology("passwords do not match")

        try:
            hash_value = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_value)

            rows = db.execute("SELECT id FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]

            flash("Registered!")
            return redirect("/")
        except:
            return apology("username already exists")
    else:
        return render_template("register.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """البحث عن سعر سهم"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if not stock:
            return apology("invalid symbol")

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """شراء الأسهم"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares_input = request.form.get("shares")

        # التحقق من الرمز
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        # التحقق من عدد الأسهم (يجب أن يكون رقماً صحيحاً موجباً)
        try:
            shares = int(shares_input)
            if shares <= 0:
                return apology("shares must be positive")
        except ValueError:
            return apology("shares must be a whole number")

        total_cost = stock["price"] * shares
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cash < total_cost:
            return apology("can't afford")

        # تحديث قاعدة البيانات
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, shares, stock["price"])

        flash(f"Bought {shares} shares of {symbol}!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """بيع الأسهم"""
    stocks = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = int(request.form.get("shares"))

        user_shares = next((s["total_shares"] for s in stocks if s["symbol"] == symbol), 0)

        if shares_to_sell > user_shares:
            return apology("too many shares")

        stock = lookup(symbol)
        revenue = stock["price"] * shares_to_sell

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -shares_to_sell, stock["price"])

        flash(f"Sold {shares_to_sell} shares of {symbol}!")
        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    """عرض سجل العمليات"""
    transactions = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """تسجيل الدخول"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return apology("must provide username and password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """تسجيل الخروج"""
    session.clear()
    return redirect("/")
