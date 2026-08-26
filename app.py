from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Database Model
class Expense(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable = False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50),nullable=False)
    expense_date = db.Column(db.String(20),nullable=False)

#Homepage
@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.id.desc()).all()
    total = sum(expense.amount for expense in expenses)
    
    return render_template("index.html", expenses = expenses, total = total)
    
#Add Expense
@app.route('/add',methods=["POST"])
def add_expense():
    
    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    expense_date = request.form["expense_date"]
    
    new_expense = Expense(
        title = title,
        amount = amount,
        category = category,
        expense_date = expense_date    
    )
    
    db.session.add(new_expense)
    db.session.commit()
    
    return redirect(url_for("index"))

#Delete Expense
@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    
    db.session.delete(expense)
    db.session.commit()
    
    return redirect(url_for("index"))

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
