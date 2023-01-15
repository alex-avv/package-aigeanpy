from math import *
from random import *
import sys

groups = 3

lines = open(sys.argv[1], 'r').readlines()

process_data=[]
for line in lines: 
  process_data.append(tuple(map(float, line.strip().split(','))))# merge the data into list

random_point=[process_data[randrange(len(process_data))], process_data[randrange(len(process_data))], process_data[randrange(len(process_data))]] # random find the piont in dataset

alloc=[]
n=0
while n<10:
  for point in process_data:
    distance2point=[None] * 3
    #find each distance to the random point of each point
    distance2point[0]=sqrt((point[0]-random_point[0][0])**2 + (point[1]-random_point[0][1])**2 + (point[2]-random_point[0][2])**2)
    distance2point[1]=sqrt((point[0]-random_point[1][0])**2 + (point[1]-random_point[1][1])**2 + (point[2]-random_point[1][2])**2)
    distance2point[2]=sqrt((point[0]-random_point[2][0])**2 + (point[1]-random_point[2][1])**2 + (point[2]-random_point[2][2])**2)
    alloc += [distance2point.index(min(distance2point))]# find the min distance index
    print(alloc)
  for i in range(3):
    alloc_process_data=[point_ for index, point_ in enumerate(process_data) if alloc[index] == i]
    new_mean=(sum([a[0] for a in alloc_process_data]) / len(alloc_process_data), sum([a[1] for a in alloc_process_data]) / len(alloc_process_data), sum([a[2] for a in alloc_process_data]) / len(alloc_process_data))
    random_point[i]=new_mean
  n=n+1

for i in range(3):
  alloc_process_data=[point_ for index, point_ in enumerate(process_data) if alloc[index] == i]
  print("Cluster " + str(i) + " is centred at " + str(random_point[i]) + " and has " + str(len(alloc_process_data)) + " points.")

  print(alloc_process_data)
