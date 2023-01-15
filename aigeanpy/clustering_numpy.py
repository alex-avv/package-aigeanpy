from math import *
from random import *
import numpy as np
from pathlib import Path


def cluster(filename, clusters, iteration):
  """numpy type kmeans file

  Parameters
  ----------
  filename :  Union(Path, str)
      the csv filename or csv file path
  clusters : int
      how many clusters we want to classify
  iteration : int
      how many times we want to repeat steps 2-3

  Raises
  ------
  TypeError
      clusters must be an int
  TypeError
      iteration must be an int
  """
  if type(clusters) is not int:
    raise TypeError('clusters must be an int')
  if type(iteration) is not int:
    raise TypeError('iteration must be an int')

  # get absolute path
  file_path_abs = sorted(Path().rglob(filename))[0]
  # read csv and return the points coords
  samples = np.loadtxt(file_path_abs, delimiter = ",")
  # random select center
  centers = samples[np.random.choice(samples.shape[0], size = clusters, replace = False)]

  samples_3d = np.expand_dims(samples, axis=1)
  samples_3d_l = np.expand_dims(samples,axis=-1)
  centers_3d = np.expand_dims(centers, axis=0)

  # iteration
  for i in range(iteration):
    # calculate the distance between all points and each center
    # squre.shape is (num_points, clusters, 3), 3 means coords xyz. 
    square = np.square(samples_3d - centers_3d)
    # distance.shape is (num_points, clusters)
    distance = np.sqrt(square.sum(axis=2))
    # get the index of the centers with the min distance from the points
    index = np.argmin(distance, axis=1)
    # change the index to one-hot-encoder, facilitate subsequent calculation
    one_hot_index = np.eye(len(df))[index][:,:clusters]
    # group_samples[k,:,i] means it the kth point belongs to the ith center. 
    # If the point do not belong to the center, then the coords=(0,0,0). 
    # If it belong to the center, then the coords= the real coords of this point
    group_samples = np.repeat(one_hot_index, 3, axis=0).reshape(len(df), 3, clusters)*samples_3d_l
    # calculate the sum of the coordinates of all the points in each cluster
    # sum.shape is (3, clusters)
    sum = np.sum(group_samples, axis=0)
    # update the center through calculate the average coords of each cluster
    centers = sum/np.sum(one_hot_index, axis=0)
    centers_3d = np.expand_dims(centers.T, axis=0)


if __name__ == "__main__":

    # Command line interface
    raise NotImplementedError
