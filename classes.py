from google.colab import auth
import gspread
from google.auth import default
import pandas as pd
from naming import SHEET, DATA_SHEET, TAGS_SHEET, Columns


class DataExpenses:
  auth.authenticate_user()
  creds, _ = default()
  CREDENTIALS = gspread.authorize(creds)

  def __init__(self):
    self.df = DataExpenses.get_data_df(self.CREDENTIALS)
    self.cols = self.df.columns.to_list()
    self.raw_df = self.df.sort_values(by=self.cols[0])
    self.df = self.raw_df.copy()
  def __repr__(self):
    return repr(self.df)
  
  def filter_by_date(self, start_date=None, end_date=None):
    if not start_date:
      start_date = self.df[self.cols[0]].min()
    if not end_date:
      end_date = self.df[self.cols[0]].max()
    self.df = self.df[(self.df[self.cols[0]] >= start_date) & (self.df[self.cols[0]] <= end_date)]
    return self
  def filter_by_tags(self, positive=[], negative=[], ALL=False):
    if positive:
      regex =DataExpenses.create_regex(positive, ALL)
      self.df = self.df[self.df[self.cols[-1]].str.contains(regex, regex=True)]
    elif negative:
      regex =DataExpenses.create_regex(negative, ALL)
      self.df = self.df[~self.df[self.cols[-1]].str.contains(regex, regex=True)]
    else:
      pass
    return self

  def group_dates(self, period):
    self.df = self.df.set_index(self.cols[0]).groupby(pd.Grouper(freq=period)).sum()
    return self

  @staticmethod
  def create_regex(word_list, ALL=False):
    if ALL:
      return "".join([f"(?=.*{word})" for word in word_list])
    else:
      return "|".join(word_list)

  @staticmethod
  def join_tags(data, index):
    return [row[:index] + [", ".join(row[index:])]  for row in data]

  @staticmethod
  def get_data_df(CREDENTIALS):
    data = CREDENTIALS.open(SHEET.NAME).worksheet(DATA_SHEET.NAME).get(DATA_SHEET.RANGE)
    columns = data[0]
    data = DataExpenses.join_tags(data[1:], len(columns)-1)
    df = pd.DataFrame(data, columns = columns)
    df[Columns.DATE] = pd.to_datetime(df[Columns.DATE], format=Columns.DATE_FORMAT)
    df[Columns.AMOUNT] = pd.to_numeric(df[Columns.AMOUNT])
    return df
