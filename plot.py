import math
import numpy as np
import matplotlib.pyplot as plt

class plot:

  def __init__(self, df):
    self.__df = df

  @staticmethod
  def __get_colors(size):
    template = ["blue", "green", "yellow", "red"]
    colors = []
    for i in range(size):
      if i < len(template):
        colors.append(template[i])
    return colors
  
  @staticmethod
  def __sum_of_prev(quantities, nbr_bef):
    sum = []
    for i in range(len(quantities[0])):
      tmp = 0
      for j in range(nbr_bef):
        tmp += quantities[j][i]
      sum.append(tmp)
    return sum

  def column_bar(self, label):
    items = list(set(self.__df[label]))
    quantities = []
    for item in items:
      quantities.append(0)
    for value in self.__df[label]:
      for i in range(len(items)):
        if items[i] == value:
          quantities[i] += 1
    plt.bar(x = items, height = quantities)
    plt.xlabel(label)
    plt.title("Column bar on " + label)
    plt.show()

  def column_bar_colors(self, label, label_color):
    items = list(set(self.__df[label]))
    color_set = list(set(self.__df[label_color]))
    quantities = []
    for i in range(len(color_set)):
      quantities.append([])
      for item in items:
        quantities[i].append(0)
    for i in range(len(self.__df[label])):
      for j in range(len(items)):
        for k in range(len(color_set)):
          if self.__df[label][i] == items[j] and self.__df[label_color][i] == color_set[k]:
            quantities[k][j] += 1
    colors = plot.__get_colors(len(color_set))
    points = []
    for i in range(len(color_set)):
      points.append(plt.bar(x = items, height = quantities[i], bottom = plot.__sum_of_prev(quantities, i), color = colors[i]))
    plt.xlabel(label)
    plt.title("Column bar on " + label + " with " + label_color)
    plt.legend(points, color_set, loc = 'lower right', title = label_color)
    plt.show()

  def hist(self, label):
    plt.hist([value for value in self.__df[label].copy() if str(value) != 'nan'], 50)
    plt.xlabel(label)
    plt.title("Histogramm on " + label)
    plt.show()

  def hist_colors(self, label, label_color):
    color_set = []
    for elem in set(self.__df[label_color]):
      color_set.append(elem)
    data = []
    for color_name in color_set:
      data.append([])
    for i in range(len(self.__df[label])):
      if not math.isnan(self.__df[label][i]):
        for j in range(len(color_set)):
          if self.__df[label_color][i] == color_set[j]:
            color_index = j
        data[color_index].append(self.__df[label][i])
    colors = plot.__get_colors(len(color_set))
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    plt.hist(data, 50, density = 1, histtype = 'bar', color = colors, stacked = True, label = color_set)
    plt.legend(loc = "lower right", title = label_color)
    plt.xlabel(label)
    plt.title("Histogramm on " + label + " with " + label_color)
    plt.show()

  def scatter(self, label_1, label_2):
    data_1 = []
    data_2 = []
    for i in range(len(self.__df[label_1])):
      if (not math.isnan(self.__df[label_1][i])) and (not math.isnan(self.__df[label_2][i])):
        data_1.append(self.__df[label_1][i])
        data_2.append(self.__df[label_2][i])
    plt.scatter(data_1, data_2)
    plt.xlabel(label_1)
    plt.ylabel(label_2)
    plt.title("Scatter plot on " + label_2 + " and " + label_1)
    plt.show()

  def scatter_colors(self, label_1, label_2, label_color):
    color_set = list(set(self.__df[label_color]))
    data_1 = []
    data_2 = []
    for color_name in color_set:
      data_1.append([])
      data_2.append([])
    for i in range(len(self.__df[label_1])):
      if (not math.isnan(self.__df[label_1][i])) and (not math.isnan(self.__df[label_2][i])):
        for j in range(len(color_set)):
          if self.__df[label_color][i] == color_set[j]:
            color_index = j
        data_1[color_index].append(self.__df[label_1][i])
        data_2[color_index].append(self.__df[label_2][i])
    colors = plot.__get_colors(len(color_set))
    points = []
    for i in range(len(color_set)):
      points.append(plt.scatter(data_1[i], data_2[i], color = colors[i]))
    plt.xlabel(label_1)
    plt.ylabel(label_2)
    plt.title("Scatter plot on " + label_2 + " and " + label_1 + " with " + label_color)
    plt.legend(points, color_set, loc = 'lower right', title = label_color)
    plt.show()

  def scatter_matrix(self):
    columns = self.__df.get_columns()
    my_dict = {}
    for i in range(len(columns)):
      my_dict[columns[i]] = self.__df[columns[i]]
    df = pd.DataFrame(my_dict, columns = columns)
    pd.plotting.scatter_matrix(df, figsize=(10, 10), hist_kwds = {'bins': 10}, s = 60, alpha = 0.8)
    plt.show()
