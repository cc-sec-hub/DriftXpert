import torch
import numpy as np
from sklearn.cluster import KMeans


class DeepCluster:
    def __init__(self,
                 encoder_flag: bool,
                 encoder_path: str,
                 n_clusters: int,
                 devive: torch.device
                 ) -> None:
        self.__encoder_flag = encoder_flag
        self.__device = devive
        self.__encoder = torch.load(encoder_path).to(self.__device)
        self.__encoder.eval()
        self.__kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)


    def fit(self, X: torch.tensor):
        if self.__encoder_flag is True:
            with torch.no_grad():
                X = X.float().to(self.__device)
                _smt = self.__encoder(X)
                self.__kmeans.fit(_smt.cpu().numpy())
        else:   
            self.__kmeans.fit(X.numpy())

    
    def predict(self, X: torch.tensor):
        if self.__encoder_flag is True:
            with torch.no_grad():
                X = X.float().to(self.__device)
                _smt = self.__encoder(X)
                return self.__kmeans.predict(_smt.cpu().numpy())
        else:
            return self.__kmeans.predict(X.numpy())


    def compute_distances_to_center(self, X: torch.tensor):
        """
        计算每个样本到其所属聚类中心的距离
        """
        if self.__encoder_flag is True:
            with torch.no_grad():
                X = X.float().to(self.__device)
                _smt = self.__encoder(X)
                _smt = _smt.cpu().numpy()
        else:
            _smt = X.numpy()

        labels = self.__kmeans.predict(_smt)

        distances = np.linalg.norm(_smt - self.__kmeans.cluster_centers_[labels], axis=1)

        distance_buckets = {i: [] for i in range(self.__kmeans.n_clusters)}
        for label, dist in zip(labels, distances):
            distance_buckets[label].append(dist)

        return distance_buckets
