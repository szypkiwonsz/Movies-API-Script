import sys

from database import Database
from movies import Movies

args = sys.argv
args = args[1:]


def script():
    # Checking if any command is typed in.
    if len(args) == 0:
        print("You have not passed any commands in! Write: python script.py --help -> show this basic help menu.")
    else:
        for a in args:
            # Getting data from api and inserting into database.
            if a == "--get_data":
                get_data = Database("movies.sqlite", "MOVIES")
                get_data.get_data()
                get_data.close()
            # Sorting movies by every column.
            elif a == "--sort_by":
                # Checking if 2nd argument is typed in.
                if sys.argv[2:]:
                    column = sys.argv[2]
                    # Checking if 2nd argument is the name of the column.
                    if column.lower() in ["id", "title", "year", "runtime", "genre", "director", "cast",
                                          "writer", "language", "country", "awards", "imdb_rating",
                                          "imdb_votes", "box_office"]:

                        sort_by = Movies("movies.sqlite", "MOVIES", column)
                        sort_by.sort_by()
                        sort_by.close()
            elif a == '--filter_by':
                if sys.argv[2:]:
                    column = sys.argv[2]
                    if sys.argv[3:]:
                        value = str(sys.argv[3])
                        if column.lower() in ["language", "director", "actor"]:
                            filter_by = Movies("movies.sqlite", "MOVIES", column)
                            filter_by.filter_by(value)
                            filter_by.close()
                        else:
                            print("This command not exist! Write: python main.py --help")
                    else:
                        if column.lower() in ["no_oscars", "awards", "box_office"]:
                            filter_by = Movies("movies.sqlite", "MOVIES", column)
                            filter_by.filter_by()
                            filter_by.close()
                        else:
                            print("This command not exist! Write: python main.py --help")
                else:
                    print("This command not exist! Write: python main.py --help")

            elif a == '--comparing_by':
                if sys.argv[2:]:
                    column = sys.argv[2]
                    if sys.argv[3:]:
                        if sys.argv[4:]:
                            first_movie = sys.argv[3]
                            second_movie = sys.argv[4]
                            if column.lower() in ["imdb_rating", "box_office", "awards", "runtime"]:
                                comparing_by = Movies("movies.sqlite", "MOVIES", column)
                                comparing_by.comparing_by(first_movie, second_movie)
                                comparing_by.close()
                            else:
                                print("This command not exist! Write: python main.py --help")
                        else:
                            print("This command not exist! Write: python main.py --help")
                    else:
                        print("This command not exist! Write: python main.py --help")
                else:
                    print("This command not exist! Write: python main.py --help")

            elif a == '--add_movie':
                if sys.argv[2:]:
                    title = sys.argv[2]
                    add_movie = Movies("movies.sqlite", "MOVIES")
                    add_movie.add_movie(title)
                    add_movie.close()
                else:
                    print("This command not exist! Write: python main.py --help")

            elif a == '--highscores':
                highscores = Movies("movies.sqlite", "MOVIES")
                highscores.highscores()
                highscores.close()


if __name__ == '__main__':
    script()
