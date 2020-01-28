import sys
import sqlite3

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
            # filtering selected movie data by argument.
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
            # comparing two selected movie data and printing the highest value.
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
            # adding movie to database.
            elif a == '--add_movie':
                if sys.argv[2:]:
                    title = sys.argv[2]
                    add_movie = Movies("movies.sqlite", "MOVIES")
                    add_movie.add_movie(title)
                    add_movie.close()
                else:
                    print("This command not exist! Write: python main.py --help")
            # printing movies data with the biggest values.
            elif a == '--highscores':
                highscores = Movies("movies.sqlite", "MOVIES")
                highscores.highscores()
                highscores.close()
            # printing available commands.
            elif a == '--help':
                print('Commands:')
                print(' --help -> show this basic help menu.')
                print(' --get_data -> Importing data from api to database.')
                print(' --sort_by COLUMN_NAME_FROM_DATABASE -> Sorting data from database by column.')
                print(' --filter_by director "NAME" -> Filtering director column by name or argument.')
                print(' --filter_by actor "NAME" -> Filtering actor column by name or argument.')
                print(' --filter_by no_oscars -> Filtering movies that was nominated.'
                      'for Oscar but did not win any.')
                print(' --filter_by awards -> Filtering movies that won more than 80% of nominations.')
                print(' --filter_by box_office -> Filtering movies that earned more than 100,000,000 $')
                print(' --filter_by language "ARGUMENT" -> Filtering language column by argument.')
                print(' --comparing_by imdb_rating "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing IMDB Rating of two movies.')
                print(' --comparing_by box_office "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Box Office of two movies.')
                print(' --comparing_by awards "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Awards of two movies.')
                print(' --comparing_by runtime "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Runtime of two movies.')
                print(' --add_movie "TITLE_OF_MOVIE" -> Adding movie with typed title.')
                print(' --highscores -> Showing current highscores in: Runtime, Box Office earnings, '
                      'Most awards won, Most nominations, Most oscars, Highest IMDB Rating.')


if __name__ == '__main__':
    try:
        script()
    except sqlite3.OperationalError as e:
        print("First you have to load data into database by writing: python main.py --get_data")
