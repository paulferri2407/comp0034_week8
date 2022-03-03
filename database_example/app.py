from pathlib import Path

from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy

# Create and configure the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(__file__).parent.joinpath('db_example.sqlite'))

# Create and configure the Flask SQLAlchemy object
db = SQLAlchemy(app)


# Create the models
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship("Post", backref=db.backref('user'))
    comments = db.relationship("Comment", backref=db.backref('user'))

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_title = db.Column(db.Text, nullable=False)
    post_text = db.Column(db.Text, nullable=False)
    comments = db.relationship("Comment", backref=db.backref('post'))

    def __repr__(self):
        return '<Post %r>' % self.post_text


class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.comment_text


@app.route('/')
def index():
    return 'This is the database example app'


if __name__ == '__main__':
    app.run(debug=True)
