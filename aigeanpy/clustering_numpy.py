# pylint: disable = W0601, W0621
import argparse
import numpy as np
from pathlib import Path
import os
CWD = Path(os.getcwd())


def cluster(filename, clusters=3, iteration=10):
    """ Numpy type kmeans file.

    Parameters
    ----------
    filename :  str
        The csv filename or csv file path.
    clusters : int
        How many clusters we want to classify.
    iteration : int
        How many times we want to repeat steps 2-3.

    Raises
    ------
    FileNotFoundError
        File '<filename>' could not be found
    TypeError
        Clusters must be an int
    TypeError
        Iteration must be an int
    """

    if __name__ == "__main__":
        global centers

    # Test to check file is in the same folder
    file_path = Path(CWD/f'{filename}')
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{filename}' could not be found")

    if not isinstance(clusters, int):
        raise TypeError("Clusters must be an int")
    if not isinstance(iteration, int):
        raise TypeError("Iteration must be an int")

    # read csv and return the points coords
    samples = np.loadtxt(filename, delimiter=",")
    # random select center
    centers = samples[np.random.choice(samples.shape[0], size=clusters,
                                       replace=False)]

    # iteration
    for k in range(iteration):
        square = np.square(np.repeat(samples, clusters, axis=0).reshape(
            samples.shape[0], clusters, samples.shape[1]) - centers)
        dist = np.sqrt(np.sum(square, axis=2))
        index = np.argmin(dist, axis=1)
        for i in range(clusters):
            centers[i] = np.mean(samples[index == i], axis=0)

    return classify_points(samples, index, clusters)


def classify_points(points, alloc, clusters):
    """ Helper function to classify the measurement points.
    """
    arr_index = np.column_stack((alloc, points))

    classify = []
    for g in range(clusters):
        classify.append(arr_index[np.where(arr_index[:, 0] == g), 1:][0])

    return classify


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Set argument.")
    parse.add_argument("file_path", type=str, help=" File of data")
    parse.add_argument("--clusters", default=3, type=int,
                       help="Clusters of k_means.")
    parse.add_argument("--iters", default=10, type=int,
                       help="Iteration of k_means.")
    parse.add_argument("--showclusters", default=False, type=bool,
                       help="Show the visual clusters or not.")
    parse.add_argument("--plotclusters", default=False, type=bool,
                       help="Plot the visual clusters or not.")
    args = parse.parse_args()

    Lclustring_point = cluster(args.file_path, args.clusters, args.iters)

    if args.showclusters is True:
        g = 0
        for p in Lclustring_point:
            print("Cluster " + str(g) + " is centred at " + str(centers[g, :])
                  + " and has " + str(len(p)) + " points.")
            print(p)
            g += 1
    else:
        g = 0
        for p in Lclustring_point:
            print("Cluster " + str(g) + " is centred at " + str(centers[g, :])
                  + " and has " + str(len(p)) + " points.")
            g += 1

    if args.plotclusters is True:
        from matplotlib import pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        for p in Lclustring_point:
            ax.scatter([a[0] for a in p], [a[1] for a in p], [a[2] for a in p])

        plt.show()
