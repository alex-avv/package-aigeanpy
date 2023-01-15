
from pathlib import Path

def kmeans(filename, clusters: int = 3, iterations: int = 10) -> list:
    
    import clustering

    clustering.cluster(filename, clusters, iterations)

    return clustering.cluster(filename, clusters, iterations)

if __name__ == '__main__':
    print(kmeans('samples1.csv'))