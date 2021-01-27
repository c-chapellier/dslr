import numpy as np

class logistic_regression:

  def __init__(self, features, labels, learning_rate = 1, iterations = 100, batch_size = 256):
    self.__learning_rate = learning_rate
    self.__iterations = iterations
    self.__batch_size = batch_size
    self.__features = features.copy()
    self.__labels = labels.copy()
    self.__features_brut = self.__features.copy()
    self.__features[:, 0] = self.__normalize(self.__features[:, 0])
    self.__features[:, 1] = self.__normalize(self.__features[:, 1])

  @staticmethod
  def __normalize(numpyArray):
    return (numpyArray - numpyArray.min(axis = 0)) / (numpyArray.max(axis = 0) - numpyArray.min(axis = 0))

  @staticmethod
  def __denormalize(numpyArray, base):
    return numpyArray * (base.max(axis = 0) - base.min(axis = 0)) + base.min(axis = 0)

  @staticmethod
  def sigmoid(scores):
    return 1 / (1 + np.exp(-scores))

  def train(self, kind = "stochastic_gradient_descent"):
    if kind == "gradient_descent":
      return self.gradient_descent()
    elif kind == "stochastic_gradient_descent":
      return self.stochastic_gradient_descent()
    raise ValueError(kind)

  def gradient_descent(self):
    size = len(self.__labels)
    y_intercept = np.ones((self.__features.shape[0], 1))
    self.__features = np.hstack((y_intercept, self.__features))
    weights = np.zeros(self.__features.shape[1])
    for step in range(self.__iterations):
      scores = np.dot(self.__features, weights)
      predictions = self.sigmoid(scores)
      errors = self.__labels - predictions
      gradients = np.dot(self.__features.T, errors)
      weights += self.__learning_rate * gradients
    # self.__features[:, 1] = self.__denormalize(self.__features[:, 1], self.__features_brut[:, 0])
    # self.__features[:, 2] = self.__denormalize(self.__features[:, 2], self.__features_brut[:, 1])
    return weights

  def stochastic_gradient_descent(self):
    size = len(self.__labels)
    y_intercept = np.ones((self.__features.shape[0], 1))
    self.__features = np.hstack((y_intercept, self.__features))
    weights = np.zeros(self.__features.shape[1])
    for step in range(self.__iterations):
      for i in range((size // self.__batch_size) + 1):
        begin = i * self.__batch_size
        end = begin + self.__batch_size
        scores = np.dot(self.__features[begin:end], weights)
        predictions = self.sigmoid(scores)
        errors = self.__labels[begin:end] - predictions
        gradients = np.dot(self.__features[begin:end].T, errors)
        weights += self.__learning_rate * gradients
    # self.__features[:, 1] = self.__denormalize(self.__features[:, 1], self.__features_brut[:, 0])
    # self.__features[:, 2] = self.__denormalize(self.__features[:, 2], self.__features_brut[:, 1])
    return weights
