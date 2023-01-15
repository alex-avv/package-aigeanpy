from math import sqrt
from random import randrange

def cluster(filename, clusters, iterations):

  lines = tool4kmeans.file_reading(filename)

  if __name__ == "__main__":
      global process_data
      global central_point

  process_data = tool4kmeans.data_loading(lines)

  central_point = tool4kmeans.create_random_point(process_data,clusters) # random find the piont in dataset
  
  alloc=[]
  n=0
  while n<iterations:
    for point in process_data:
      #find each distance to the random point of each point
      Ldistance = tool4kmeans.distance2points(point,central_point)
      alloc.append(tool4kmeans.min_index(Ldistance))# find the min distance index
    for g in range(clusters):
      alloc_process_data=tool4kmeans.group_datas(g,process_data,alloc)
      new_mean=(sum([a[0] for a in alloc_process_data]) / len(alloc_process_data), 
      sum([a[1] for a in alloc_process_data]) / len(alloc_process_data), 
      sum([a[2] for a in alloc_process_data]) / len(alloc_process_data))
      central_point[g]=new_mean
    n=n+1


  return tool4kmeans.classify_points(process_data,alloc,clusters)


class tool4kmeans:
#with safty open
  def file_reading(file_path):
    with open(file_path, 'r') as file:
      lines = file.readlines()
    return lines

  def data_loading(lines):
    process_data=[]
    for line in lines: 
      process_data.append(tuple(map(float, line.strip().split(','))))# merge the data into list
    return process_data

  def create_random_point(Lpoint,groups):
    return [Lpoint[randrange(len(Lpoint))] for g in range(groups)]

  def distance2points(point1,Lpoint2):
    Ldistance2point = []
    for point in Lpoint2:
      Ldistance2point.append(sqrt((point1[0]-point[0])**2 + (point1[1]-point[1])**2 + (point1[2]-point[2])**2))
    return Ldistance2point

  def min_index(list):
    return list.index(min(list))

  def group_datas(group,Lprocess_data,alloc):
    group_data = []
    for j, p in enumerate(Lprocess_data):
      if alloc[j]==group:
        group_data.append(p)
    return group_data

  def classify_points(points,alloc,clusters):
    classified_clusters = []
    for g in range(clusters):
      alloc_process_data = tool4kmeans.group_datas(g,process_data,alloc)
      classified_clusters.append(alloc_process_data)
    
    return classified_clusters

    


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
      print("Cluster " + str(g) + " is centred at " + str(central_point[g]) + " and has " + str(len(p)) + " points.")
      print(p)
      g += 1



  if args.plotclusters == True:
    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for p in Lclustring_point:
      ax.scatter([a[0] for a in p],[a[1] for a in p],[a[2] for a in p])
    
    plt.show()

