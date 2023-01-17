import os
from pathlib import Path
import time
import shutil
import numpy as np
from matplotlib import pyplot as plt
from aigeanpy import analysis


def create_file(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print('--- new folder done ---')

    else:
        print("--there is this folder--")


def create_random_point(number):
    return np.random.random((number, 3))


# Create a filder to save the sample cas
create_file('./sample')

# Create the range of the point
number_range = np.arange(1000, 10500, 500)

# create the sample csv
for n in number_range:
    np.savetxt(f'./sample/sample_{n}.csv',
               create_random_point(n), delimiter=',')


# sort csv file name by natural number
files = [str(f) for f in Path().glob('./sample/*.csv')]
files.sort(key=lambda x: int(x.split('_')[1][:-4]))

# measure the time
Ltime_clustering = []

for file in files:
    start = time.time()
    analysis.kmeans(file)
    end = time.time()
    Ltime_clustering.append(end-start)

Ltime_clustering_numpy = []

for file in files:
    start = time.time()
    analysis.kmeans(file, isNumpy=True)
    end = time.time()
    Ltime_clustering_numpy.append(end-start)

# remove the sample file
shutil.rmtree('./sample')

# plot the compare figure
plt.plot(number_range, Ltime_clustering, "r-",
         label='clustering.py')
plt.plot(number_range, Ltime_clustering_numpy, "b-",
         label='clustering_numpy.py')
plt.xlabel('N points')
plt.ylabel('Time taken of each N')
plt.title('Time taken comparison')
plt.legend()
plt.savefig('performance.png')
plt.show()

# save figure
