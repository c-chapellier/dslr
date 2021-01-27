import numpy as np

from my_list import my_list
from plot import plot

class my_dataframe:

  def __init__(self, dataset_path):
    self.__columns = []
    self.__float_columns = []
    self.__values = []
    self.__values_types = []
    self.__init_from_csv(dataset_path)
  
  def __init_from_csv(self, dataset_path):
    with open(dataset_path, "r") as file:
      lines = file.read().splitlines()
    self.__columns = lines[0].split(',')
    for i in range(len(self.__columns)):
      self.__values.append(my_list())
      self.__values_types.append("float")
    for line in lines[1:]:
      split = line.split(',')
      for i in range(len(split)):
        try:
          tmp = float(split[i])
        except ValueError:
          tmp = str(split[i])
          if tmp == "":
            tmp = np.nan
          else:
            self.__values_types[i] = "string"
        self.__values[i].append(tmp)
    for i in range(len(self.__columns)):
      if self.__values_types[i] == "string":
        for value in self.__values[i]:
          value = str(value)
      else:
        self.__float_columns.append(self.__columns[i])
    self.plot = plot(self)

  def __getitem__(self, key):
    for i in range(len(self.__columns)):
      if self.__columns[i] == key:
        return self.__values[i]
    raise ValueError(key)

  def get_columns(self):
    return self.__columns

  def __iter(self, name):
    value = name[:6]
    print(value + ((8 - len(value)) * ' '), end = '')
    for column in self.__float_columns:
      if name == "count":
        value = str(self[column].count())[:12]
      elif name == "mean":
        value = str(self[column].mean())[:12]
      elif name == "std":
        value = str(self[column].std())[:12]
      elif name == "min":
        value = str(min(self[column]))[:12]
      elif name == "25%":
        value = str(self[column].percentile(25))[:12]
      elif name == "50%":
        value = str(self[column].percentile(50))[:12]
      elif name == "75%":
        value = str(self[column].percentile(75))[:12]
      elif name == "max":
        value = str(max(self[column]))[:12]
      else:
        raise ValueError(name)
      print(value + ((16 - len(value)) * ' '), end = '')
    print()

  def describe(self):
    print(8 * ' ', end = '')
    for label in self.__float_columns:
      value = label[:12]
      print(value + ((16 - len(value)) * ' '), end = '')
    print()
    self.__iter("count")
    self.__iter("mean")
    self.__iter("std")
    self.__iter("min")
    self.__iter("25%")
    self.__iter("50%")
    self.__iter("75%")
    self.__iter("max")
