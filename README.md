### A script created in python that downloads data from the "OMDb API" once and uploads it to a SQLite database filled only with movie titles. Using commands we operate on data in the database, i.e. we sort, filter by language, etc.

##### Avaible commands below.

##### The script do:
- Inserts data from "OMDb API" into database filled only with titles of the movies.
- You can add movie only with title value and then again you can insert data from "OMDb API" to update values in database.
- Sorts every movie in database by selected column.
- Filters movies by:
  Director, 
  Actor, 
  Movies that was nominated  for oscar but did not win any, 
  Movies that won more than 80% of nominations, 
  Movies that earned more than 100,000,000$,
  Only movies in certain Language.
- Compares by:
  IMDb Rating,
  Box office earnings,
  Number of awards won,
  Runtime.
- Adds movie to database.
- Shows current highscores in:
  Runtime,
  Box office earnings,
  Most awards won,
  Most nominations,
  Most Oscars,
  Highest IMDB Rating.

##### The script checks: 
- If the user has entered wrong command.
- If the user has entered command before he loads data into database.

##### Avaible commands:

python script.py COMMAND

--help -> show basic help menu.

--get_data -> Importing data from api to database. 

--sort_by COLUMN_NAME_FROM_DATABASE -> Sorting data from database by column.

--filter_by director "NAME" -> Filtering director column by name or argument. 

--filter_by actor "NAME" -> Filtering actor column by name or argument. 

--filter_by no_oscars -> Filtering movies that was nominated for Oscar but did not win any. 

--filter_by awards -> Filtering movies that won more than 80% of nominations. 

--filter_by box_office -> Filtering movies that earned more than 100,000,000 $ 

--filter_by language "ARGUMENT" -> Filtering language column by argument. 

--comparing_by imdb_rating "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing IMDB Rating of two selected movies. 

--comparing_by box_office "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Box Office of selected two movies. 

--comparing_by awards "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Awards of two selected movies. 

--comparing_by runtime "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Runtime of two selected movies. 

--add_movie "TITLE_OF_MOVIE" -> Adding movie with typed title. 

--highscores -> Showing current highscores in: Runtime, Box Office earnings, Most awards won, 
Most nominations, Most oscars, Highest IMDB Rating.

##### Packages to install:
- pip install requests

##### Version of software used:
- Python 3.7.x
