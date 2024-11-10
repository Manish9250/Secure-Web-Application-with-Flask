from backend import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), default=1000)
    # Backref used to get owners list which own a certain item
    items = db.relationship("Item", backref="owned_user", lazy=True) # Relatioship for getting owned items from user

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")
        
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def pretty_budget(self):
        money = str(self.budget)
        if len(money) >= 4:
            return f'{money[:-3]},{money[-3:]}'
        else:
            return money

    def can_buy(self, item):
        return self.budget >= item.price
    
    def can_sell(self, item):
        return item in self.items






class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    desc = db.Column(db.String(length=500), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))


    def item_assigned(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def item_deassigned(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()


