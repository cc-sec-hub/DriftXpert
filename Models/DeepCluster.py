import torch
import numpy as np
from sklearn.cluster import KMeans


class DeepCluster:
    def __init__(self,
                 encoder_path: str,
                 encoder_flag: bool,
                 n_clusters: int,
                 devive: torch.device
                 ) -> None:
        self.__device = devive
        self.__encoder_flag = encoder_flag
        self.__encoder = torch.load(encoder_path).to(self.__device)
        self.__encoder.eval()
        self.__kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
        self.__column_mask = [0, 1, 3, 5, 6, 10, 16, 17, 18, 25, 26, 27, 28, 30]


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
                _smt = _smt.cpu().numpy()  # 转换为 NumPy 数组
        else:
            _smt = X.numpy()

        # 获取每个样本的聚类标签
        labels = self.__kmeans.predict(_smt)  # 获取每个样本的聚类标签

        # 计算每个样本到其所属聚类中心的欧氏距离
        distances = np.linalg.norm(_smt - self.__kmeans.cluster_centers_[labels], axis=1)

        # 将距离按标签分桶
        distance_buckets = {i: [] for i in range(self.__kmeans.n_clusters)}
        for label, dist in zip(labels, distances):
            distance_buckets[label].append(dist)

        return distance_buckets
