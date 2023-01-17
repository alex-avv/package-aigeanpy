from aigeanpy import clustering, clustering_numpy

def kmeans(filename, clusters = 3, iterations = 10, isNumpy = False):
    """ Forms clusters from the specified points using the kmeans algorithm.

    Parameters
    ----------
    filename : str
        Path to the CSV file with the points to be grouped.
    clusters : int, optional
        Number of clusters, by default 3.
    iterations : int, optional
        Number of iterations for the algorithm, by default 10.
    isNumpy : bool, optional
        Specify whether to use the numpy version, by default False.

    Returns
    -------
    list
        With the indices of the points for each group.
    """

    if isNumpy == False:
        return clustering.cluster(filename, clusters, iterations)

    if isNumpy == True:
        return clustering_numpy.cluster(filename, clusters, iterations)
