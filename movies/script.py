import click

from data_loader import JsonLoader
from database import DatabaseHandler
from query_handler import QueryHandler, SortByValuesHandler, FilterByValueHandler, FilterByNominatedForOscarHandler, \
    FilterByWinsNominationsHandler, FilterByBoxOfficeHandler, CompareByImdbRatingHandler, CompareByBoxOfficeHandler, \
    CompareByAwardsWonHandler, CompareByRuntimeHandler, HighScoreByRuntimeHandler, \
    HighScoreByBoxOfficeHandler, HighScoreByAwardsWonHandler, HighScoreByNominationsHandler, \
    HighScoreByOscarsWonHandler, HighScoreByImdbRatingHandler


@click.group()
def cli():
    pass


@cli.command(help='Loads movies data from api to database.')
def load_from_api():
    temp_query_handler = QueryHandler()
    temp_json_loader = JsonLoader()
    temp_json_loader.load_movies_data(temp_query_handler.get_all_titles())
    temp_query_handler.update_movies(temp_json_loader.data)
    click.echo('The database has been updated.')


@cli.command(help='Add entered movie from api to database.')
@click.argument('title', nargs=1, type=str)
def add_movie(title):
    temp_json_loader = JsonLoader()
    temp_json_loader.load_movie_from_api(title)
    temp_database_handler = DatabaseHandler()
    temp_database_handler.insert_movies(temp_json_loader.data)
    click.echo(f'{title} movie has been added correctly.')


@cli.command(help='Sorts movies against the entered table names.')
@click.argument('table_names', nargs=-1, type=str)
def sort_by(table_names):
    temp_sort_handler = SortByValuesHandler()
    click.echo(temp_sort_handler.sort_by_selected_columns(table_names))


@cli.command(help='Filters movies by entered table name and value.')
@click.argument('arguments', nargs=2, type=str)
def filter_by(arguments):
    temp_filter_handler = FilterByValueHandler()
    click.echo(temp_filter_handler.get_filtered_movies_by_value(arguments[0], arguments[1]))


@cli.command(help='Filters movies which was nominated for oscar but did not win any.')
def filter_by_no_oscars():
    temp_filter_handler = FilterByNominatedForOscarHandler()
    click.echo(temp_filter_handler.get_filtered_movies_by_nomination_for_oscar())


@cli.command(help='Filters movies which has more wins than 80% of nominations.')
def filter_by_wins_nominations():
    temp_filter_handler = FilterByWinsNominationsHandler()
    click.echo(temp_filter_handler.get_filtered_movies_by_wins_nominations())


@cli.command(help='Filters movies which has box office larger than 100.000.000$.')
def filter_by_box_office():
    temp_filter_handler = FilterByBoxOfficeHandler()
    click.echo(temp_filter_handler.get_filtered_movies_by_box_office())


@cli.command(help='Compares movies by imdb rating value.')
@click.argument('movie_titles', nargs=2, type=str)
def compare_by_imdb_rating(movie_titles):
    temp_compare_by_imdb_rating_handler = CompareByImdbRatingHandler()
    click.echo(temp_compare_by_imdb_rating_handler.get_compared_movies_by_imdb_rating(movie_titles[0], movie_titles[1]))


@cli.command(help='Compares movies by box office value.')
@click.argument('movie_titles', nargs=2, type=str)
def compare_by_box_office(movie_titles):
    temp_compare_by_box_office_handler = CompareByBoxOfficeHandler()
    click.echo(temp_compare_by_box_office_handler.get_compared_movies_by_box_office(movie_titles[0], movie_titles[1]))


@cli.command(help='Compares movies by awards won.')
@click.argument('movie_titles', nargs=2, type=str)
def compare_by_awards_won(movie_titles):
    temp_compare_by_awards_won_handler = CompareByAwardsWonHandler()
    click.echo(temp_compare_by_awards_won_handler.get_compared_movies_by_awards_won(movie_titles[0], movie_titles[1]))


@cli.command(help='Compares movies by runtime.')
@click.argument('movie_titles', nargs=2, type=str)
def compare_by_runtime(movie_titles):
    temp_compare_by_runtime_handler = CompareByRuntimeHandler()
    click.echo(temp_compare_by_runtime_handler.get_compared_movies_by_runtime(movie_titles[0], movie_titles[1]))


@cli.command(help='Shows highscores in selected columns.')
def highscores():
    click.echo(f'Runtime: {HighScoreByRuntimeHandler().get_movie_high_score_by_runtime()}'),
    click.echo(f'Box Office: {HighScoreByBoxOfficeHandler().get_movie_high_score_by_box_office()}'),
    click.echo(f'Awards Won: {HighScoreByAwardsWonHandler().get_movie_with_most_awards_won()}'),
    click.echo(f'Nominations: {HighScoreByNominationsHandler().get_movie_with_most_nominations()}'),
    click.echo(f'Oscars: {HighScoreByOscarsWonHandler().get_movie_with_most_oscars_won()}'),
    click.echo(f'IMDB Rating: {HighScoreByImdbRatingHandler().get_movie_high_score_by_imdb_rating()}')


if __name__ == '__main__':
    cli()
