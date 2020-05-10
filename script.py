from database import Api
from movies import SortBy, FilterBy, CompareBy, AddMovie, Highscores
import argparse
import time

if __name__ == '__main__':
    # start = time.perf_counter()

    API_KEY = '39f41e43'
    DB_NAME = 'movies.sqlite'

    parser = argparse.ArgumentParser()
    parser.add_argument('--get_data', action='store_true',
                        help='download all movies')
    parser.add_argument('--sort_by', help='sort movies by column')
    parser.add_argument('--filter_by', nargs='+', help='sort movies by column')
    parser.add_argument('--compare_by', nargs='+', help='comparing movies by column')
    parser.add_argument('--add_movie', help='adding movie by title')
    parser.add_argument('--highscores', action='store_true', help='shows highscores')
    args = parser.parse_args()

    if not any(vars(args).values()):
        print('There are no arguments passed!')
    elif args.get_data:
        api = Api(DB_NAME, API_KEY)
        api.update_database()
    elif args.sort_by:
        sort_by = SortBy(DB_NAME, args.sort_by)
        sort_by.sort_by()
    elif args.filter_by:
        filter_by = FilterBy(DB_NAME, args.filter_by)
        filter_by.filter_by()
    elif args.compare_by:
        compare_by = CompareBy(DB_NAME, args.compare_by)
        compare_by.compare_by()
    elif args.add_movie:
        add_movie = AddMovie(DB_NAME, API_KEY, args.add_movie)
        add_movie.add_movie()
        del add_movie
        add_movie = AddMovie(DB_NAME, API_KEY, args.add_movie)
        add_movie.update_database()
    elif args.highscores:
        highscores = Highscores(DB_NAME)
        highscores.highscores()
        # finish = time.perf_counter()
        # print(f'Finished in {round(finish-start, 2)} second(s)')
