from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

#CREATE DATABAE
app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///Movie.db"
db = SQLAlchemy(app)
#Optional:  This will silence the deprecation warning in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)

db.create_all()

#CREATE FORM
#ADD FORM
class  Add_movie(FlaskForm):
    title = StringField("Movie title", validators=[DataRequired()])
    year = StringField("Year",validators=[DataRequired()] )
    description = StringField("Description", validators=[DataRequired()])
    rating = StringField("Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    img_url = StringField("Image link", validators=[DataRequired()])
    submit = SubmitField(label='Submit')

#EDIT FORM
class  Edit_movie(FlaskForm):
    rating = StringField("Rating")
    review = StringField("Review")
    submit = SubmitField(label='Submit')

@app.route("/")
def home():
    #Sorting by rating
    all_movies = db.session.query(Movie).order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    all_movies = db.session.query(Movie).order_by(Movie.ranking).all()
    return render_template("index.html", movies=all_movies)

@app.route("/add", methods=["GET", 'POST'])
def add():
    form = Add_movie()
    if form.validate_on_submit():
        title = form.title.data
        print(title)

        exist = Movie.query.filter_by(title=form.title.data).first() is not None
        if not exist:
            #ADD NEW RECORD
            new_movie = Movie(
                title = form.title.data,
                year = form.year.data,
                description = form.description.data,
                rating = form.rating.data,
                ranking = 10,
                review = form.review.data,
                img_url = form.img_url.data,
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect( url_for('home'))

    return render_template("add.html", form=form)

@app.route("/delete/<id_num>")
def delete(num_id):

    movie_to_delete = Movie.query.filter_by(id=num_id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()

    return render_template("index.html")

@app.route("/edit/<id_num>", methods=["GET", 'POST'])
def edit(id_num):
    # print(id_num)
    Movie_to_update = Movie.query.filter_by(id=id_num).first()
    
    form = Edit_movie()
    if form.validate_on_submit():
        if form.review.data is not "":
            Movie_to_update.review = form.review.data
        if form.rating.data is not "":
            Movie_to_update.rating = form.rating.data

        db.session.commit()
        return redirect( url_for("home"))
        
    return render_template("edit.html", movie=Movie_to_update, form=form)

if __name__ == '__main__':
    app.run(debug=True)
