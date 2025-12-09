from eta import app,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey("user.id") )
        
    def __repr__(self):
        return f"Expense('{self.category}','{self.title}','{self.amount}')"
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable= False)
    email = db.Column(db.String, nullable = False)
    password_hash= db.Column(db.String, nullable = False)
    expenses = db.relationship("Expense", backref = "owner", lazy = True)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    
    def __repr__(self):
        return f"User('{self.name}','{self.email}')"