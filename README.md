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

### Avaible commands

Sorting movie data by every column

```
python script.py --sort_by [column_name]
```
---

Filtering movies data

```
python script.py --filter_by director "[parameter]"
```
```
python script.py --filter_by cast "[parameter]"
```
```
python script.py --filter_by cast "[parameter]"
```
```
python script.py --filter_by no_oscars ---> Filtering movies that was nominated for Oscar but did not win any.
```
```
python script.py --filter_by awards ---> Filtering movies that won more than 80% of nominations.
```
```
python script.py --filter_by box_office ---> Filtering movies that earned more than $100,000,000
```
---

Comparing two movies by selected columns

```
python script.py --compare_by imdb_rating [first_movie] [second_movie]
```
```
python script.py --compare_by box_office [first_movie] [second_movie]
```
```
python script.py --compare_by awards [first_movie] [second_movie]
```
```
python script.py --compare_by runtime [first_movie] [second_movie]
```
---

Adding movie by title and updating data if exist

```
python script.py --add_movie [movie title]
```
---

```
python script.py --highscores ---> Showing highscores in: Runtime, Box Office, Awards, Nominations, Oscars, Imdb Rating.
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
Open terminal with choosen folder "Movies-API-Script>"
```
```
Type selected command
```
---
## Built With

* [Python 3.7](https://www.python.org/) - The programming language used

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The script was made as a recruitment task for an internship
