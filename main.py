from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Create database
with app.app_context():
    db.create_all()

# Home Page
@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date_created.desc()).all()
    total = sum(exp.amount for exp in expenses)
    highest = max([exp.amount for exp in expenses], default=0)
    avg = total / len(expenses) if expenses else 0
    return render_template("index.html",
                           expenses=expenses,
                           total=total,
                           highest=highest,
                           avg=avg)

# Add expense
@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form["title"]
    amount = float(request.form["amount"])
    new_expense = Expense(title=title, amount=amount)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for("index"))

# Delete expense
@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
