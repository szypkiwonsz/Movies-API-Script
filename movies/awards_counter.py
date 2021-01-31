class MovieAwards:
    """Class representing movie awards."""

    def __init__(self, movie):
        self.movie = movie
        self.oscars_nominations = 0
        self.oscars_wins = 0
        self.wins = 0
        self.nominations = 0


class AwardsCounter(MovieAwards):
    """Inheriting class storing methods for scraping awards from data about movie."""

    def scrape_awards(self):
        """Scrape movie awards by data."""
        self.scrape_oscar_wins()
        self.scrape_oscar_nominations()
        self.scrape_wins()
        self.scrape_nominations()

    def scrape_oscar_wins(self):
        """Scrapes oscar wins from movie data."""
        if 'Won' in self.movie['awards'] and 'Oscar' in self.movie['awards']:
            self.oscars_wins = int(self.movie['awards'].split(' ')[1])

    def scrape_oscar_nominations(self):
        """Scrapes oscar nominations from movie data."""
        if 'Nominated' in self.movie['awards'] and 'Oscar' in self.movie['awards']:
            self.oscars_nominations = int(self.movie['awards'].split(' ')[2])

    def scrape_wins(self):
        """Scrape award wins from movie data."""
        if 'wins' in self.movie['awards']:
            wins_word_index = self.movie['awards'].replace('.', '').split(' ').index('wins')
            self.wins = int(self.movie['awards'].split(' ')[wins_word_index - 1])

    def scrape_nominations(self):
        """Scrape award nominations from movie data."""
        if 'Nominated' in self.movie['awards'] and not 'Oscar' in self.movie['awards']:
            self.nominations = int(self.movie['awards'].split(' ')[2])
        if 'nominations' in self.movie['awards']:
            nominations_word_index = self.movie['awards'].replace('.', '').split(' ').index('nominations')
            self.nominations = int(self.movie['awards'].split(' ')[nominations_word_index - 1])
