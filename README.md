<b>script.py</b>  
<font color="#ff0000">ONLY ARGUMENTS IN --comparing_by HAVE TO BE WRITTEN IN QUOTES!</font>
 
<b>Avaible commands:</b>

--help -> show basic help menu.

--get_data -> Importing data from api to database. 

--sort_by COLUMN_NAME_FROM_DATABASE -> Sorting data from database by column. 

--filter_by director NAME -> Filtering director column by name or argument. 

--filter_by actor NAME -> Filtering actor column by name or argument. 

--filter_by no_oscars -> Filtering movies that was nominated for Oscar but did not win any. 

--filter_by awards -> Filtering movies that won more than 80% of nominations. 

--filter_by box_office -> Filtering movies that earned more than 100,000,000 $ 

--filter_by language ARGUMENT -> Filtering language column by argument. 

--comparing_by imdb_rating "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing IMDB Rating of two selected movies. 

--comparing_by box_office "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Box Office of selected two movies. 

--comparing_by awards "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Awards of two selected movies. 

--comparing_by runtime "FIRST_MOVIE" "SECOND_MOVIE" -> Comparing Runtime of two selected movies. 

--add_movie TITLE_OF_MOVIE -> Adding movie with typed title. 

--highscores TITLE_OF_MOVIE -> Showing current highscores in: Runtime, Box Office earnings, Most awards won, 
Most nominations, Most oscars, Highest IMDB Rating. 
