import pandas as pd
import csv
from naming import SHEET, DATA_SHEET, Columns


class DataExpenses:
    TESTING_DATA_FILE = "test_data/data_test.csv"

    def __init__(self, TESTING=False):
        data = self.get_data(TESTING)
        self.df = DataExpenses.transform_data_to_df(data)
        self.cols = self.df.columns.to_list()
        self.raw_df = self.df.sort_values(by=self.cols[0])
        self.df = self.raw_df.copy()

    def __repr__(self):
        return repr(self.df)

    def recover_raw(self):
        self.df = self.raw_df.copy()
        return self

    def filter_by_date(self, start_date=None, end_date=None):
        if not start_date:
            start_date = self.df[self.cols[0]].min()
        if not end_date:
            end_date = self.df[self.cols[0]].max()
        self.df = self.df[
            (self.df[self.cols[0]] >= start_date) & (self.df[self.cols[0]] <= end_date)
        ]
        return self

    def filter_by_tags(self, positive=[], negative=[], ALL=False):
        if positive:
            regex = DataExpenses.create_regex(positive, ALL)
            self.df = self.df[self.df[self.cols[-1]].str.contains(regex, regex=True)]
        elif negative:
            regex = DataExpenses.create_regex(negative, ALL)
            self.df = self.df[~self.df[self.cols[-1]].str.contains(regex, regex=True)]
        else:
            pass
        return self

    def group_dates(self, period):
        self.df = self.df.set_index(self.cols[0]).groupby(pd.Grouper(freq=period)).sum()
        return self

    @staticmethod
    def get_data(TESTING=False):
        if not TESTING:
            CREDENTIALS = DataExpenses.get_google_credentials()
            data = (
                CREDENTIALS.open(SHEET.NAME)
                .worksheet(DATA_SHEET.NAME)
                .get(DATA_SHEET.RANGE)
            )
        else:
            with open(DataExpenses.TESTING_DATA_FILE, "r") as read_obj:
                csv_reader = csv.reader(read_obj)
                data = list(csv_reader)
            data = [list(filter(None, row)) for row in data]

        return data

    @staticmethod
    def get_google_credentials():

        from google.colab import auth
        import gspread
        from google.auth import default

        auth.authenticate_user()
        creds, _ = default()
        return gspread.authorize(creds)

    @staticmethod
    def create_regex(word_list, ALL=False):
        if ALL:
            return "".join([f"(?=.*{word})" for word in word_list])
        else:
            return "|".join(word_list)

    @staticmethod
    def join_tags(data, index):
        final_rows = []
        for row in data:
            unique_tags = set(row[index:])
            join_tags = ", ".join(unique_tags)
            final_rows.append(row[:index] + [join_tags])
        return final_rows

    @staticmethod
    def transform_data_to_df(data):
        columns = data[0]
        data = DataExpenses.join_tags(data[1:], len(columns) - 1)
        df = pd.DataFrame(data, columns=columns)
        df[Columns.DATE] = pd.to_datetime(df[Columns.DATE], format=Columns.DATE_FORMAT)
        df[Columns.AMOUNT] = pd.to_numeric(df[Columns.AMOUNT])
        df = df[~(df[Columns.TAGS] == "")]
        return df
