# Movies-API-Script

A script created in Python that downloads data from the "OMDb API" once and uploads it to a SQLite database filled only with movie titles. Using commands we operate on data in the database, i.e. we sort, filter by language, etc.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Libraries and Packages

```
pip install -r requirements.txt
```
---
### Running

A step by step series of examples that tell you how to run a script

```
Download project
```
```
Install requirements
```
```
Open terminal with choosen folder "Movies-API-Script\movies>"
```
```
Type selected command
```
---
### Running tests

How to run tests
```
Do the same as for running the script
```
```
Open terminal with choosen folder "Movies-API-Script>"
```
```
Type: pytest -v or pytest -v --cov=movies (to check coverage of tests)
```
---
### Available commands

Sorting movie data by one or multiple columns

```
python script.py sort-by column_name(s)
```
---

Filtering movies data

```
python script.py filter-by director "parameter" -> Filtering movies by director
```
```
python script.py filter-by cast "parameter" -> Filtering movies by actor
```
```
python script.py filter-by language "parameter" -> Filtering movies only in certain language
```
```
python script.py filter-by-no-oscars ---> Filtering movies that was nominated for Oscar but did not win any.
```
```
python script.py filter-by-wins-nominations ---> Filtering movies that won more than 80% of nominations.
```
```
python script.py filter-by-box-office ---> Filtering movies that earned more than $100,000,000
```
---

Comparing two movies by selected columns

```
python script.py compare_by-imdb-rating "first_movie" "second_movie"
```
```
python script.py compare-by-box-office "first_movie" "second_movie"
```
```
python script.py compare-by-awards-won "first_movie" "second_movie"
```
```
python script.py compare-by-runtime "first_movie" "second_movie"
```
---

Adding movie by title and updating data if exist

```
python script.py add-movie "movie title"
```
---

```
python script.py highscores ---> Showing highscores in: Runtime, Box Office, Awards, Nominations, Oscars, Imdb Rating.
```
---
## Built With

* [Python 3.7](https://www.python.org/) - The programming language used

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The script was made as a recruitment task for an internship
