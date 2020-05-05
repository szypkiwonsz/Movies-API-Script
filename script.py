from database import Api
from movies import SortBy, FilterBy
import argparse
import time

if __name__ == "__main__":
    start = time.perf_counter()

    API_KEY = '39f41e43'
    DB_NAME = 'movies.sqlite'

    parser = argparse.ArgumentParser()
    parser.add_argument("--get_data", action='store_true',
                        help="download all movies")
    parser.add_argument("--sort_by", help="sort movies by column")
    parser.add_argument("--filter_by", nargs='+', help="sort movies by column")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print("There are no arguments passed!")
    elif args.get_data:
        api = Api(DB_NAME, API_KEY)
        api.update_database()
    elif args.sort_by:
        sort_by = SortBy('movies.sqlite', args.sort_by)
        sort_by.sort_by()
    elif args.filter_by:
        filter_by = FilterBy('movies.sqlite', args.filter_by)
        filter_by.filter_by()
        finish = time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} second(s)')