# Movies-API-Script

A script created in Python that downloads data from the "OMDb API" once and uploads it to a SQLite database filled only with movie titles. Using commands we operate on data in the database, i.e. we sort, filter by language, etc.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

requests

```
pip install requests
```
---

### Avaible commands

Sorting movie data by column

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


### Running


