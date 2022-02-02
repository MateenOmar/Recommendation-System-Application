import random


class User:
    def __init__(user, number):
        user.__number = number
        user.__movies = {}
        user.__genres = {}

    def addMovie(user, movie, rating, genres):
        user.__movies[movie] = rating

        for genre in genres:

            if user.__genres.get(genre) is None:
                user.__genres[genre] = 0

            user.__genres[genre] = user.__genres[genre] + rating / 5

    def getMovies(user):
        return user.__movies

    def getRating(user, movie):
        return user.__movies.get(movie)

    def getRatedGenres(user):
        genres = sorted(user.__genres.items(),
                        key=lambda x: x[1], reverse=True)

        return dict(genres)

    def getFavouriteGenres(user):
        keys = list(user.__genres.items())
        random.shuffle(keys)
        d = dict(keys)

        genres = sorted(d.items(), key=lambda x: x[1], reverse=True)

        favGenres = []

        for i in genres:
            favGenres.append(i[0])

        return favGenres[0: -(len(genres) // -4)]

    def computeMovieSimilarity(user, user2, movie):
        if user2.getRating(movie) is not None:
            return user.getRating(movie) / user2.getRating(movie)

        return 0.0

    def computeMoviesSimilarity(user, user2):
        total = 0
        count = 0

        for x in user.__movies:
            if user2.getRating(x) is not None:
                total = total + user.getRating(x) / user2.getRating(x)
                count = count + 1

        if count != 0:
            total = total / count

        return [total, count]

    def similarGenres(user, db):

        sim = db.getSimilarGenreMovies(user.getFavouriteGenres())

        for movie in sim:
            if movie in user.__movies:
                sim.remove(movie)

        return sim

    def similarMovie(user, db, movie, year):
        sim = db.getSimilarMovies(
            movie, year, user.getRating(movie + " (" + str(year) + ")"))

        for movie in sim:
            if movie in user.__movies:
                sim.remove(movie)

        return sim
