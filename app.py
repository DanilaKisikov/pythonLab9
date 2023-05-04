from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

with app.app_context():
    my_file = Path("data.db")
    if not my_file.is_file():
        db.create_all()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Double, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articleId = db.Column(db.Integer, primary_key=False)
    autor = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Double, nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id


@app.route('/')
def mainPage():
    return render_template('mainPage.html')


@app.route('/createArticle')
def creatingPage():
    return render_template('creatingPage.html')


@app.route('/Article/<string:name>')
def articlePage(name):
    return "Article: " + name


if __name__ == '__main__':
    app.run(debug=True)
