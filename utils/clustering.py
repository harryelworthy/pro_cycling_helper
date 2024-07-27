from sklearn.cluster import DBSCAN
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, f1_score
from sklearn.metrics import homogeneity_score, completeness_score, v_measure_score
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN


def test_clustering(y_true,y_pred):
    # Evaluating the clustering performance
    ari = adjusted_rand_score(y_true, y_pred)
    nmi = normalized_mutual_info_score(y_true, y_pred)
    homogeneity = homogeneity_score(y_true, y_pred)
    completeness = completeness_score(y_true, y_pred)
    v_measure = v_measure_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')

    print(f"Adjusted Rand Index (ARI): {ari}")
    print(f"Normalized Mutual Information (NMI): {nmi}")
    print(f"Homogeneity: {homogeneity}")
    print(f"Completeness: {completeness}")
    print(f"V-measure: {v_measure}")
    print(f"F1 Score: {f1}")

def k_distance_graph(projections):
    # Use NearestNeighbors to find the k-nearest neighbors (k = min_samples)
    k = 5  # Or any other value for min_samples
    nearest_neighbors = NearestNeighbors(n_neighbors=k)
    neighbors = nearest_neighbors.fit(projections)
    distances, indices = neighbors.kneighbors(projections)

    # Sort the distances and plot
    distances = np.sort(distances[:, k-1], axis=0)
    plt.plot(distances)
    plt.title('k-distance Graph')
    plt.xlabel('Points sorted by distance to {}-th nearest neighbor'.format(k))
    plt.ylabel('Distance to {}-th nearest neighbor'.format(k))
    plt.show()

def dbscan_cluster(projections, eps, min_samples):
    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    y_pred = dbscan.fit_predict(projections)

    # Return the predicted labels
    return y_pred

def plot_cluster(projections, y_pred, title=""):
    # Plot the clusters
    plt.figure(figsize=(10, 6))
    plt.scatter(projections[:, 0], projections[:, 1], c=y_pred, cmap='viridis')
    plt.title(title)
    plt.xlabel('Projection 1')
    plt.ylabel('Projection 2')
    plt.colorbar(label='Cluster')
    plt.grid(False)