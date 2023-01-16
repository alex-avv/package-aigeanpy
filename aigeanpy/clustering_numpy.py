from math import *
from random import *
import numpy as np

def cluster(filename, clusters=3, iteration=10):


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

    if __name__ == "__main__":
        global centers

    if type(clusters) is not int:
        raise TypeError('clusters must be an int')
    if type(iteration) is not int:
        raise TypeError('iteration must be an int')

    # read csv and return the points coords
    samples = np.loadtxt(filename, delimiter = ",")
    # random select center
    centers = samples[np.random.choice(samples.shape[0], size = clusters, replace = False)]

    # iteration
    for k in range(iteration):
        square = np.square(np.repeat(samples, clusters, axis=0).reshape(samples.shape[0], clusters, samples.shape[1]) - centers)
        dist = np.sqrt(np.sum(square, axis=2))
        index = np.argmin(dist, axis=1)
        for i in range(clusters):
            centers[i] = np.mean(samples[index == i], axis=0)

    return classify_points(samples,index,clusters)


def classify_points(points,alloc,clusters):

    arr_index = np.column_stack((alloc,points))

    classify = []
    for g in range(clusters):
        arr_index[np.where(arr_index[:,0]==0),1:][0]
        classify.append(arr_index[np.where(arr_index[:,0] == g),1:][0])

    return classify

if __name__ == "__main__":


  import argparse

  parse = argparse.ArgumentParser(description= 'set argument')
  parse.add_argument('file_path', type = str ,help = ' file of data')
  parse.add_argument('--clusters',default = 3, type = int, help = ' clusters of k_means' )
  parse.add_argument('--iters', default= 10, type = int, help = ' iteration of k_means')
  parse.add_argument('--showclusters', default = False, type = bool, help=' show the visual clusters or not')
  parse.add_argument('--plotclusters', default = False, type = bool, help =' plot the visual clusters or not')

  args = parse.parse_args()

  Lclustring_point = cluster(args.file_path,args.clusters,args.iters)
  
  if args.showclusters == True:
    g = 0
    for p in Lclustring_point:
      print("Cluster " + str(g) + " is centred at " + str(centers[:,g]) + " and has " + str(len(p)) + " points.")
      print(p)
      g += 1

  if args.plotclusters == True:
    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for p in Lclustring_point:
      ax.scatter([a[0] for a in p],[a[1] for a in p],[a[2] for a in p])
    
    plt.show()

