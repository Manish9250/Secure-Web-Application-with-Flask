from flask import render_template, redirect, url_for, flash, request
from backend import app, db
from backend.modals import Item, User
from backend.forms import RegistrationForm, LoginForm, BuyForm, SellForm, PaymentForm
from flask_login import login_user, logout_user, login_required, current_user



@app.route("/")
def home_page():
    return render_template('index.html')
    


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    buy_form = BuyForm()
    sell_form = SellForm()
    # Buying an item
    if request.method == "POST":
        buyed_item = request.form.get("buyed_item") #Grabed the name of item form html page
        obj_buyed_item = Item.query.filter_by(name=buyed_item).first() #Grabed the object of that item
        if obj_buyed_item:
            if current_user.can_buy(obj_buyed_item):
                obj_buyed_item.item_assigned(current_user)

                flash("Item Bougnt Successfully.", category="success")
            else:
                flash("Need More Money.", category="info")

    # Selling an item
        sold_item = sell_form.owned_item_name.data
        obj_sold_item = Item.query.filter_by(name=sold_item).first()
        print(obj_sold_item)
        if obj_sold_item:
            if current_user.can_sell(obj_sold_item):
                obj_sold_item.item_deassigned(current_user)

                flash("Item sold Successfully.", category="success")
            else:
                flash("Dear Customer firstly buy the item.", category="info")

        
        return redirect(url_for("market_page"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, owned_items=owned_items, buy_form=buy_form, sell_form=sell_form)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user )
            return redirect(url_for("market_page"))
        else:
            flash("Username or Password is incorrect.", category="danger")

    return render_template('login.html', form=form)


@app.route("/signup", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm() # Created a instance of registeration form

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password = form.pwd1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully.", category="info")
        
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category="danger")

    return render_template("signup.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")

    return redirect(url_for("home_page"))

@app.route("/add_money", methods=["GET", "POST"])
def add_money_page():
    payment_form = PaymentForm()

    if request.method == "POST":
        amount = payment_form.amount.data
        current_user.budget += int(amount)
        db.session.commit()

        flash(f"{amount} added to your account.")

        return redirect(url_for("market_page"))
        
    return render_template("payment.html", payment_form=payment_form)

