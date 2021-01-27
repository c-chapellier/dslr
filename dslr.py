import sys
import pandas as pd

from my_dataframe import my_dataframe
from one_vs_all import one_vs_all
        
if __name__ == "__main__":
  argc = len(sys.argv)
  if argc < 2:
    print("arg[1] must be datascience or logistic_regression")
    exit()

  if sys.argv[1] == "datascience":
    df = my_dataframe("./datasets/dataset_train.csv")
    # df.plot.scatter_matrix()
    # for i in range(len(df._float_labels)):
    #   for j in range(len(df._float_labels)):
    #     if i < j:
    #       df.plot.scatter(df._float_labels[i], df._float_labels[j])
    #   df.plot.hist_colors(df._float_labels[i], "Hogwarts House")
    df.plot.column_bar("Hogwarts House")
    df.plot.column_bar("Best Hand")
    df.plot.column_bar_colors("Best Hand", "Hogwarts House")
    df.plot.column_bar_colors("Hogwarts House", "Best Hand")
    df.plot.hist("Transfiguration")
    df.plot.hist_colors("Transfiguration", "Best Hand")
    df.plot.scatter("Transfiguration", "Potions")
    df.plot.scatter_colors("Transfiguration", "Potions", "Hogwarts House")
    df.describe()
    print("-------- Real --------")
    df2 = pd.read_csv("./datasets/dataset_train.csv")  
    print(df2.describe())

  elif sys.argv[1] == "logistic_regression":
    df = my_dataframe("./datasets/dataset_train.csv")
    df.plot.scatter_colors("Astronomy", "Ancient Runes", "Hogwarts House")
    model = one_vs_all(df, "Astronomy", "Ancient Runes")
    model.train()
    model.test("./datasets/dataset_train.csv")
    model.test_subject("./datasets/dataset_test.csv", "Astronomy", "Ancient Runes")

  else:
    print("arg[1] must be datascience or logistic_regression")
