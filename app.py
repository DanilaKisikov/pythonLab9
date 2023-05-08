from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


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
        return '<Comment %r>' % self.articleId


@app.route('/', methods=['POST', 'GET'])
def mainPage():
    if request.method == "POST":
        comments = Comment.query.all()
        articles = Article.query.all()

        for com in comments:
            db.session.delete(com)
        for art in articles:
            db.session.delete(art)

        db.session.commit()
        return redirect('/')

    else:
        articles = Article.query.order_by(Article.date.desc()).all()
        if articles is not None:
            return render_template('mainPage.html', articles=articles)
        else:
            return render_template('mainPage.html')


@app.route('/createArticle', methods=['POST', 'GET'])
def creatingPage():
    if request.method == "POST":
        name = request.form['name']
        text = request.form['text']
        autor = request.form['autor']

        article = Article(autor=autor, name=name, text=text, points=0)

        try:
            db.session.add(article)
            db.session.commit()
            print(article.name + ' created!')
            return redirect('/')
        except:
            return "Ошибочка"
    else:
        return render_template('creatingPage.html')


@app.route('/articlePage/<int:id>', methods=['POST', 'GET'])
def articlePage(id):
    if request.method == "POST":
        article = Article.query.get(id)

        autor = request.form['autor']
        text = request.form['text']
        try:
            score = int(request.form['rating'])
        except:
            score = 1

        comment = Comment(autor=autor, text=text, points=score, articleId=id)

        comments = Comment.query.filter_by(articleId=id).order_by(Comment.date.desc()).all()
        if comments is not None:
            summ = score
            for com in comments:
                summ += com.points

            thisScore = summ / (len(comments) + 1)
            article.points = thisScore
        else:
            article.points = score

        try:
            db.session.add(comment)
            db.session.commit()
            return redirect('/articlePage/' + str(id))
        except:
            return "Ошибочка"
    else:
        article = Article.query.get(id)
        comments = Comment.query.filter_by(articleId=id).order_by(Comment.date.desc()).all()
        print(comments)

        if comments is not None:
            print('hello')
            return render_template('articlePage.html', article=article, comments=comments)
        else:
            return render_template('articlePage.html', article=article)


if __name__ == '__main__':
    with app.app_context():
        my_file = Path("instance/data.db")
        if not my_file.is_file():
            print('db created')
            db.create_all()

    app.run(debug=True)
