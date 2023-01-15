from math import *
from random import *
import numpy as np
import clustering

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

    if __name__ == "__main__":
        global centers

    if type(clusters) is not int:
        raise TypeError('clusters must be an int')
    if type(iteration) is not int:
        raise TypeError('iteration must be an int')

    # read csv
    lines = clustering.tool4kmeans.file_reading(filename)

    # change to numpy
    samples = np.array(clustering.tool4kmeans.data_loading(lines))
    samples_3d = np.expand_dims(samples, axis=1)
    samples_3d_l = np.expand_dims(samples,axis=-1)

    # random select center, and change to numpy
    row_rand_array = np.arange(samples.shape[0])
    np.random.shuffle(row_rand_array)
    centers = samples[row_rand_array[0:clusters]]
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
        one_hot_index = np.eye(samples.shape[0])[index][:,:clusters]


    # group_samples[k,:,i] means it the kth point belongs to the ith center. 
    # If the point do not belong to the center, then the coords=(0,0,0). 
    # If it belong to the center, then the coords= the real coords of this point
        group_samples = np.repeat(one_hot_index, 3, axis=0).reshape(samples.shape[0], 3, clusters)*samples_3d_l


    # calculate the sum of the coordinates of all the points in each cluster
    # sum.shape is (3, clusters)
        sum = np.sum(group_samples, axis=0)

    # update the center through calculate the average coords of each cluster
        centers = sum/np.sum(one_hot_index, axis=0)
        centers_3d = np.expand_dims(centers.T, axis=0)

    # arr_index = np.column_stack((index,samples))
    # print(arr_index[np.where(arr_index[:,0]==0),1:][0])


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
