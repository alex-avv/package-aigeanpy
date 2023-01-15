
from pathlib import Path

def kmeans(filename, clusters: int = 3, iterations: int = 10, isNumpy = False) -> list:
    
    if isNumpy == False:
        import clustering

        return clustering.cluster(filename, clusters, iterations)
    
    if isNumpy == True:
        import clustering_numpy

        return clustering_numpy.cluster(filename, clusters, iterations)

if __name__ == '__main__':
    print(kmeans('samples1.csv'))