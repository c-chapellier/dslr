import math

class my_list(list):

    def __len__(self):
      i = 0
      for value in self:
        i += 1
      return i

    def __min__(self):
      min = float("inf")
      for value in self:
        if not math.isnan(value):
          if value < min:
            min = value
      return min

    def __max__(self):
      max = float("-inf")
      for value in self:
        if not math.isnan(value):
          if value > max:
            max = value
      return max

    def count(self):
      i = 0
      for value in self:
        if not math.isnan(value):
          i += 1
      return i

    def mean(self):
      mean = 0.0
      size = self.count()
      for value in self:
        if not math.isnan(value):
          mean += value / size
      return mean
    
    def variance(self):
      dev = 0.0
      mean = self.mean()
      for value in self:
        if not math.isnan(value):
          dev += (value - mean) ** 2
      return dev / (self.count() - 1)

    def std(self):
      return self.variance() ** 0.5

    def sort(self):
      size = len(self)
      if size > 1:
        mid = size // 2
        lefthalf = self[:mid]
        righthalf = self[mid:]
        lefthalf.sort()
        righthalf.sort()
        i = 0 ; j = 0 ; k = 0     
        while i < len(lefthalf) and j < len(righthalf):
          if lefthalf[i] < righthalf[j]:
            self[k] = lefthalf[i]
            i += 1
          else:
            self[k]=righthalf[j]
            j += 1
          k += 1
        while i < len(lefthalf):
          self[k] = lefthalf[i]
          i += 1
          k += 1
        while j < len(righthalf):
          self[k] = righthalf[j]
          j += 1
          k += 1
      return self

    def percentile(self, th):
      ordered = [value for value in self.copy() if str(value) != 'nan']
      ordered.sort()
      n = math.ceil((th / 100) * len(ordered))
      down = n - 1
      while down >= 0 and math.isnan(ordered[down]):
        down -= 1
      up = n
      while up < len(self) and math.isnan(ordered[up]):
        up += 1
      return (ordered[down] + ordered[up]) / 2