from flask import Flask, render_template, redirect, url_for, request
from user import User
from movieDB import Movies
import csv

moviesDB = Movies()
users = {}


def readCSV():
    with open("ml-25m/movies.csv", "r", encoding="utf-8") as movies:
        reader = csv.reader(movies)
        next(reader, None)

        for x in reader:
            moviesDB.addMovie(int(x[0]), x[1], x[2])

    with open("ml-25m/ratings.csv", "r", encoding="utf-8") as ratings:
        reader = csv.reader(ratings)
        next(ratings, None)

        for x in reader:
            usrNum = int(x[0])
            nameWYear = moviesDB.getNameWithYear(int(x[1]))

            if users.get(usrNum) is None:
                users[usrNum] = User(usrNum)

            users[usrNum].addMovie(nameWYear,
                                   float(x[2]),
                                   moviesDB.getGenres(nameWYear),
                                   )
            moviesDB.addRating(int(x[1]), float(x[2]))


app = Flask(__name__)

app.secret_key = b'key'

current_user = 0


@app.teardown_appcontext
def close_connection(exception):
    return 1


@app.route('/', methods=['GET', 'POST'])
def load():
    readCSV()
    return redirect(url_for('signIn'))


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    return render_template("signIn.html")


@app.route('/home', methods=['GET', 'POST'])
def home():
    global current_user

    current_user = int(request.form['userID'])
    return redirect(url_for('homePage'))


@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
    return render_template("home.html", userID=current_user)


@app.route('/movies', methods=['GET', 'POST'])
def moviesList():
    moviesL = moviesDB.getMovies()
    return render_template("movies.html", userID=current_user, movies=moviesL)


@app.route('/info', methods=['GET', 'POST'])
def myInfo():

    moviesL = users[current_user].getMovies()
    favGenres = users[current_user].getFavouriteGenres()
    ratedGenres = users[current_user].getRatedGenres()

    return render_template("info.html", userID=current_user, movies=moviesL, favGenres=favGenres, ratedGenres=ratedGenres)


@app.route('/recommendMovie', methods=['GET', 'POST'])
def recommendationOnMovies():

    movieName = request.form['movieName']
    movieYear = int(request.form['movieYear'])

    moviesL = users[current_user].similarMovie(moviesDB, movieName, movieYear)

    return render_template("recommendation.html", userID=current_user, movie=movieName, year=movieYear, movies=moviesL)


@app.route('/recommendGenre', methods=['GET', 'POST'])
def recommendationOnGenres():
    moviesL = users[current_user].similarGenres(moviesDB)

    return render_template("recommendation.html", userID=current_user, movie='', year='', movies=moviesL)


@app.route('/movieRating', methods=['GET', 'POST'])
def movieRating():

    movieName = request.form['movieNameR']
    movieYear = request.form['movieYearR']

    rating = moviesDB.getRating(movieName + " (" + movieYear + ")")
    numPpl = moviesDB.getMovie(movieName, movieYear)[3]

    return render_template("movieRating.html", userID=current_user, movie=movieName, year=movieYear, movieRating=rating, num=numPpl)


@app.route('/similarityRating', methods=['GET', 'POST'])
def similarityRating():

    user2ID = int(request.form['user2ID'])
    movieName = request.form['movieName']
    movieYear = request.form['movieYear']

    similarity = users[current_user].computeMovieSimilarity(
        users[user2ID], movieName + " (" + movieYear + ")")
    moviesL = users[current_user].similarMovie(moviesDB, movieName, movieYear)

    return render_template("similarityRating.html", userID=current_user, user2ID=user2ID, movie=movieName, year=movieYear, similarity=similarity,  movies=moviesL)


@app.route("/<name>")
def error(name):
    return "ERROR: Incorrect page"


if __name__ == "__main__":
    app.run(debug=True)
