from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = Book(
            title=request.form["title"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()

        # redirect to the home page after the form has been submitted.
        return redirect(url_for('home'))

    return render_template("add.html")


@app.route('/retrieve')
def retrieve():
    all_books = db.session.query(Book).all()
    return render_template("retrieve.html", books=all_books)


if __name__ == "__main__":
    app.run(debug=True)

