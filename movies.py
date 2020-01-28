from database import Database


class Movies(Database):
    def __init__(self, name, table, column=None):
        super().__init__(name, table)
        self.titles = Database.select(self, "TITLE")
        if column is not None:
            if column.upper() == "NO_OSCARS":
                self.data_column = Movies.get(self, "AWARDS")
            else:
                self.data_column = Movies.get(self, column)
        self.column = column

    # Inserting titles and selected movie data into dictionary.
    def get(self, column):

        data = {}
        all_data = Database.select(self, "*")
        for movies in range(len(self.titles)):
            if column.upper() == "ID":
                data[self.titles[movies][0]] = all_data[movies][0]
            elif column.upper() == "TITLE":
                data[self.titles[movies][0]] = all_data[movies][1]
            elif column.upper() == "YEAR":
                data[self.titles[movies][0]] = all_data[movies][2]
            elif column.upper() == "RUNTIME":
                data[self.titles[movies][0]] = all_data[movies][3]
            elif column.upper() == "GENRE":
                data[self.titles[movies][0]] = all_data[movies][4]
            elif column.upper() == "DIRECTOR":
                data[self.titles[movies][0]] = all_data[movies][5]
            elif column.upper() == "CAST":
                data[self.titles[movies][0]] = all_data[movies][6]
            elif column.upper() == "WRITER":
                data[self.titles[movies][0]] = all_data[movies][7]
            elif column.upper() == "LANGUAGE":
                data[self.titles[movies][0]] = all_data[movies][8]
            elif column.upper() == "COUNTRY":
                data[self.titles[movies][0]] = all_data[movies][9]
            elif column.upper() == "AWARDS":
                data[self.titles[movies][0]] = all_data[movies][10]
            elif column.upper() == "IMDB_RATING":
                data[self.titles[movies][0]] = all_data[movies][11]
            elif column.upper() == "IMDB_VOTES":
                data[self.titles[movies][0]] = all_data[movies][12]
            elif column.upper() == "BOX_OFFICE":
                data[self.titles[movies][0]] = all_data[movies][13]
        return data

    # Getting dictionary with one selected column and titles column.
    @staticmethod
    def dictionary(keys, values):
        data = {}
        for i in range(len(keys)):
            data[keys[i]] = values[i]
        return data

    # Checking if column values are int or string type.
    def string_or_int(self):
        if self.column.upper() in ["ID", "YEAR", "RUNTIME", "IMDB_RATING", "IMDB_VOTES", "BOX_OFFICE"]:
            return True
        else:
            return False

    # Converting matrix to cleaned int.
    def int(self):
        matrix_values = []
        matrix_keys = []
        if self.column.upper() in ["IMDB_VOTES", "RUNTIME", "BOX_OFFICE"]:
            for value in self.data_column.values():
                value = ''.join(value for value in str(value) if value.isdigit())
                matrix_values.append(value)
            for key in self.data_column.keys():
                matrix_keys.append(key)
            matrix = Movies.dictionary(matrix_keys, matrix_values)
            return matrix
        else:
            return self.data_column

    # Cleaning matrix for string.
    @staticmethod
    def matrix_cleaning(matrix):
        cleaned_matrix = []
        for data in matrix:
            cleaned_matrix.append(data[0])
        return cleaned_matrix

    # Sorting method.
    def sorting(self):
        data = sorted(self.data_column.items(), key=lambda kv: (kv[1], kv[0]))
        return data

    # Reversed sorting method.
    def sorting_reverse(self):
        data = sorted(self.data_column.items(), key=lambda kv: (float(kv[1]) if kv[1] else 0, kv[0]), reverse=True)
        return data

    def hours_minutes(self, data_column):
        if data_column is not "":
            minutes = int(data_column) % 60
            hours = int(data_column) // 60
            cleaned_data = str(hours) + "h " + str(minutes) + "min"
        else:
            cleaned_data = ""
        return cleaned_data

    def dollar_char(self, data):
        if data is not "":
            cleaned_data = "$" + data
        else:
            cleaned_data = ""
        return cleaned_data

    def comma(self, data_column):
        if data_column is not "":
            value = '{:,}'.format(int(data_column))
        else:
            value = ""
        return value

    def printing(self, highscores=False):
        print("{}".format(150 * "-"))
        if highscores is False:
            print("{}{}{}".format("TITLE", 47 * " ", self.column.upper()))
        else:
            print("{}{}{}".format(self.column.upper(), 45 * " ", "TITLE"), 45 * " ", "VALUE")
        print("{}".format(150 * "-"))
        for i in range(len(self.data_column)):
            if self.column.upper() == "RUNTIME":
                cleaned_data = Movies.hours_minutes(self, self.data_column[i][1])
            elif self.column.upper() == "BOX_OFFICE" or self.column.upper() == "IMDB_VOTES":
                values = Movies.comma(self, self.data_column[i][1])
                if self.column.upper() == "BOX_OFFICE":
                    cleaned_data = Movies.dollar_char(self, values)
                else:
                    cleaned_data = values
            else:
                cleaned_data = self.data_column[i][1]
            if highscores is False:
                print(self.data_column[i][0], (50 - len(self.data_column[i][0])) * " ", str(cleaned_data))
        if highscores is True:
            cleaned_data = Movies.hours_minutes(self, self.data_column[0][1])
            print(self.column.upper(), (50 - len(self.column.upper())) * " ", self.data_column[0][0],
                  (50 - len(self.data_column[0][0])) * " ", cleaned_data)

    def awards(self):
        awards = {}
        for key, value in self.data_column.items():
            oscars_won, oscars_nominated, won, wins, nominations, nominated = 0, 0, 0, 0, 0, 0
            value = value.split()
            if 'Won' in value:
                won = value[value.index("Won") + 1]
                if "Oscars." in value or "Oscar." in value:
                    oscars_won = value[value.index("Won") + 1]
            if "wins" in value:
                wins = value[value.index("wins") - 1]
            if "nominations." in value:
                nominations = value[value.index("nominations.") - 1]
            if "Nominated" in value:
                nominated = value[value.index("Nominated") + 2]
                if "Oscars." in value or "Oscar." in value:
                    oscars_nominated = value[value.index("Nominated") + 2]
            awards[key] = won, wins, nominations, nominated, oscars_won, oscars_nominated
        return awards

    # --sort_by
    def sort_by(self, highscores=False):
        # Checking if column values are int or string.
        val = Movies.string_or_int(self)
        if val is True:
            # Method converting int to string.
            self.data_column = Movies.int(self)
        if self.column.upper() in ["IMDB_RATING", "IMDB_VOTES", "RUNTIME", "BOX_OFFICE", "YEAR"]:
            # if selected column sort from the biggest to the lowest.
            self.data_column = Movies.sorting_reverse(self)
        else:
            self.data_column = Movies.sorting(self)
        if highscores is False:
            Movies.printing(self)
        else:
            return self.data_column

    # --filter_by
    def filter_by(self, parameter=None):
        dictionary = {}
        if self.column.upper() == "BOX_OFFICE":
            self.data_column = Movies.int(self)
            for key, value in self.data_column.items():
                if value is not "":
                    if int(value) > 100000000:
                        dictionary[key] = value
        elif self.column.upper() == "AWARDS":
            awards = Movies.awards(self)
            self.column = "AWARDS WON"
            for key, value in awards.items():
                wins = int(value[0]) + int(value[1])
                nominations = (int(value[2]) + int(value[3]))
                if wins > nominations * 0.8:
                    dictionary[key] = wins
        elif self.column.upper() == "NO_OSCARS":
            self.column = "AWARDS"
            awards = Movies.awards(self)
            print(awards)
            self.column = "OSCAR NOMINATIONS"
            for key, value in awards.items():
                print(key, value[4], value[5])
                if int(value[5]) > 0 and int(value[4]) == 0:
                    dictionary[key] = str(value[5]) + " oscar nominations."
        else:
            self.data_column = dict(self.data_column)
            for key, value in self.data_column.items():
                if parameter in value:
                    dictionary[key] = value

        self.data_column = dictionary
        self.data_column = list(self.data_column.items())
        Movies.printing(self)

    # --comparing_by
    def comparing_by(self, first_movie, second_movie):
        data = {}
        if self.column.upper() == "AWARDS":
            cleaned_data = Movies.awards(self)
            wins_first = int(cleaned_data[first_movie][0]) + int(cleaned_data[first_movie][1])
            wins_second = int(cleaned_data[second_movie][0]) + int(cleaned_data[second_movie][1])
            if wins_first > wins_second:
                data[first_movie] = wins_first
            else:
                data[second_movie] = wins_second
        else:
            cleaned_data = Movies.int(self)
            if (cleaned_data[first_movie]) > (cleaned_data[second_movie]):
                data[first_movie] = cleaned_data[first_movie]
            else:
                data[second_movie] = cleaned_data[second_movie]
        self.data_column = list(data.items())
        Movies.printing(self)

    # --add_movie
    def add_movie(self, title):
        Movies.insert(self, title)
        print("Correctly added movie: {}.".format(title))

    def highscores(self):
        self.column = "RUNTIME"
        self.data_column = Movies.get(self, "RUNTIME")
        self.data_column = Movies.sort_by(self, True)
        Movies.printing(self, True)







