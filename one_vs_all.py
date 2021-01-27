import math
import numpy as np
import matplotlib.pyplot as plt

from my_dataframe import my_dataframe
from logistic_regression import logistic_regression

class one_vs_all:

  def __init__(self, df, column_1, column_2, learning_rate = 1, iterations = 100, batch_size = 256):
    self.__column_1 = column_1
    self.__column_2 = column_2
    self.__learning_rate = learning_rate
    self.__iterations = iterations
    self.__batch_size = batch_size
    self.__value_1 = df[column_1].copy()
    self.__value_2 = df[column_2].copy()
    self.__houses = df["Hogwarts House"].copy()
    self.__weights = [None] * 4
    self.__save = [None] * 4
    self.__rm_nan()

  @staticmethod
  def __normalize(numpyArray, base):
    return (numpyArray - base.min(axis = 0)) / (base.max(axis = 0) - base.min(axis = 0))

  @staticmethod
  def __denormalize(numpyArray, base):
    return numpyArray * (base.max(axis = 0) - base.min(axis = 0)) + base.min(axis = 0)

  def __rm_nan(self):
    size = len(self.__value_1)
    for i in range(size):
      j = size - i - 1
      if math.isnan(self.__value_1[j]) or math.isnan(self.__value_2[j]):
        self.__value_1.pop(j)
        self.__value_2.pop(j)
        self.__houses.pop(j)
    return self

  def __get_labels(self, my_house):
    tmp = []
    for i in range(len(self.__houses)):
      if self.__houses[i] == my_house:
        tmp.append(0)
      else:
        tmp.append(1)
    return np.array(tmp)

  def train(self):
    houses_set = list(set(self.__houses))
    for i in range(len(houses_set)):
      features = np.vstack((np.array(self.__value_1, dtype=np.float128), np.array(self.__value_2, dtype=np.float128))).T
      labels = self.__get_labels(houses_set[i])
      model = logistic_regression(features, labels, self.__learning_rate, self.__iterations, self.__batch_size)
      self.__weights[i] = model.train()
      self.__save[i] = features.copy()

      # features[:, 0] = self.__normalize(features[:, 0], self.__save[i][:, 0])
      # features[:, 1] = self.__normalize(features[:, 1], self.__save[i][:, 1])
      # data = np.hstack((np.ones((features.shape[0], 1)), features))
      # scores = np.dot(data, self.__weights[i])
      # preds = np.round(logistic_regression.sigmoid(scores))
      # print('Accuracy for ' + houses_set[i] + ': ' + str((preds == labels).sum() / len(preds)))
      # features[:, 0] = self.__denormalize(features[:, 0], self.__save[i][:, 0])
      # features[:, 1] = self.__denormalize(features[:, 1], self.__save[i][:, 1])
      # plt.scatter(features[:, 0], features[:, 1], c = (preds == labels))
      # plt.show()

  def predict(self, value_1, value_2):
    houses_set = list(set(self.__houses))
    scores = [None] * len(houses_set)
    for i in range(len(houses_set)):
      normalize_1 = self.__normalize(value_1, self.__save[i][:, 0])
      normalize_2 = self.__normalize(value_2, self.__save[i][:, 1])
      data = np.hstack((1, normalize_1, normalize_2))
      scores[i] = np.dot(data, self.__weights[i])
      # print(str(i) + " " + str(scores[i]))
    # print(scores)
    # print(houses_set)
    min = float("+inf")
    min_house = None
    for i in range(len(houses_set)):
      if scores[i] < min:
        min = scores[i]
        min_house = houses_set[i]
    # print(np.round(logisticRegression.sigmoid(min)))
    return min_house

  def test(self, dataset_test_path):
    df_test = my_dataframe(dataset_test_path)
    good = 0
    sum = 0
    nan = 0
    colors = []
    for i in range(len(df_test["Hogwarts House"])):
      if (not math.isnan(df_test[self.__column_1][i])) and (not math.isnan(df_test[self.__column_2][i])):
        pred = self.predict(df_test[self.__column_1][i], df_test[self.__column_2][i])
        if pred == df_test["Hogwarts House"][i]:
          good += 1
          colors.append(1)
        else:
          colors.append(0)
        #   print("Index = " + str(i))
        #   print("Bad house: " + str(df_test[self.__column_1][i]) + " and " + str(df_test[self.__column_2][i]))
        #   print(pred, end = '')
        #   print(" vs " + str(df_test["Hogwarts House"][i]))
      else:
        colors.append(0)
        nan += 1
      sum += 1
    print("Test accuracy = " + str(good / (sum - nan)) + " with nan = " + str(nan / sum))
    plt.scatter(df_test["Astronomy"], df_test["Ancient Runes"], c = colors)
    plt.show()

  def test_subject(self, dataset_test_path, column_1, column_2):
    df_test = my_dataframe(dataset_test_path)
    preds = []
    for i in range(len(df_test["Hogwarts House"])):
      if (not math.isnan(df_test[column_1][i])) and (not math.isnan(df_test[column_2][i])):
        preds.append(self.predict(df_test[column_1][i], df_test[column_2][i]))
    with open("houses.csv", "w") as file:
      file.write("Index,Hogwarts House\n")
      for i in range(len(preds)):
        file.write(str(i) + "," + str(preds[i] + "\n"))
