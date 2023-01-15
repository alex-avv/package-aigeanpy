from math import sqrt
from random import randrange
import sys

groups = 3
interations =10
file_path = sys.argv[1]

#with safty open
def file_reading(file_path):
  with open(sys.argv[1], 'r') as file:
    lines = file.readlines()
  return lines

def data_loading(lines):
  process_data=[]
  for line in lines: 
    process_data.append(tuple(map(float, line.strip().split(','))))# merge the data into list
  return process_data


lines = file_reading(file_path)
process_data = data_loading(lines)

central_point=[process_data[randrange(len(process_data))] for g in range(groups)] # random find the piont in dataset

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

#[(),()]

alloc=[]
n=0
while n<interations:
  for point in process_data:
    #find each distance to the random point of each point
    Ldistance = distance2points(point,central_point)
    alloc.append(min_index(Ldistance))# find the min distance index
  for g in range(groups):
    alloc_process_data=group_datas(g,process_data,alloc)
    new_mean=(sum([a[0] for a in alloc_process_data]) / len(alloc_process_data), sum([a[1] for a in alloc_process_data]) / len(alloc_process_data), sum([a[2] for a in alloc_process_data]) / len(alloc_process_data))
    central_point[g]=new_mean
  n=n+1

for g in range(groups):
  alloc_process_data = group_datas(g,process_data,alloc)
  print("Cluster " + str(g) + " is centred at " + str(central_point[g]) + " and has " + str(len(alloc_process_data)) + " points.")

  print(alloc_process_data)

