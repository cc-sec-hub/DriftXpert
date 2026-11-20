import torch
import numpy as np
import pandas as pd
from Config import *
from Models.DeepCluster import DeepCluster
from Trainer.Datasets import DataSets
from sklearn.metrics import classification_report


def cls_report(y, preds, title):
    report = classification_report(y, preds, digits=4)
    print(title)
    print(report)


if __name__ == '__main__':
    torch.manual_seed(1234)

    n_clusters = 5
    
    no_cuda = False
    cuda_available = not no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if cuda_available else "cpu")

    _data = DataSets()
    _model = DeepCluster(encoder_flag=True, encoder_path=l0main_set1_model_path[1], 
                         n_clusters=n_clusters, devive=device)

    TrainX, TestX, TrainY, TestY = _data.LoadDataset(global_drift_set1_path, test_size=0.2)

    _model.fit(TrainX)
    PredsY = _model.predict(TestX)
    PredsY = pd.DataFrame(PredsY)
    print(PredsY.value_counts())

    distance_buckets = _model.compute_distances_to_center(TestX)
    mean = []
    std = []
    for i in range(n_clusters):
        mean.append(np.mean(distance_buckets[i]))
        std.append(np.std(distance_buckets[i]))
    
    # 输出每个聚类桶中距离是否大于均值
    for i in range(n_clusters):
        if len(distance_buckets[i]) > 0:
            print(f"Cluster {i}: Sum of distances > mean: {np.sum(distance_buckets[i] > mean[i] + std[i])}")
        else:
            print(f"Cluster {i}: No data in this cluster")

    TestX, TestY = _data.LoadDataset(global_drift_set2_path)
    PredsY = _model.predict(TestX)
    PredsY = pd.DataFrame(PredsY)
    print(PredsY.value_counts())
    distance_buckets = _model.compute_distances_to_center(TestX)
    # 输出每个聚类桶中距离是否大于均值
    for i in range(n_clusters):
        if len(distance_buckets[i]) > 0:
            print(f"Cluster {i}: Sum of distances > mean: {np.sum(distance_buckets[i] > mean[i]+ std[i])}")
        else:
            print(f"Cluster {i}: No data in this cluster")
