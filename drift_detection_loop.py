import torch
import numpy as np
import pandas as pd
from Config import *
from Trainer.Datasets import DataSets
from Models.DeepCluster import DeepCluster


log_K = []
log_OR = []

def compute_or(outliers, shape):
    return ((1 / shape[0]) * outliers[0]) / ((1 / shape[1]) * outliers[1])


def do_loop(K, alpha):
    no_cuda = False
    cuda_available = not no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if cuda_available else "cpu")

    _data = DataSets()
    model = DeepCluster(encoder_flag=True, encoder_path=l0main_set1_model_path[1],
                        n_clusters=K, devive=device)

    # load historical data
    TrainX, TestX, _, _ = _data.LoadDataset(local_drift_set1_path, test_size=0.2)
    model.fit(TrainX)

    TestX, _ = _data.LoadDataset(local_drift_set1_path)
    distance_buckets = model.compute_distances_to_center(TestX)
    _historical_samples = TestX.shape[0]

    mean = []
    std = []
    for i in range(K):
        mean.append(np.mean(distance_buckets[i]))
        std.append(np.std(distance_buckets[i]))

    # 标记离群点
    _historical_outliers = 1
    for i in range(K):
        if len(distance_buckets[i]) > 0:
            _historical_outliers += np.sum(distance_buckets[i] > mean[i] + alpha * std[i])
        else:
            print(f"Cluster {i}: No data in this cluster")

    # load recent data
    TestX, _ = _data.LoadDataset(local_drift_set2_path)

    distance_buckets = model.compute_distances_to_center(TestX)
    _recent_samples = TestX.shape[0]

    # 输出每个聚类桶中距离是否大于均值
    _recent_outliers = 1
    for i in range(K):
        if len(distance_buckets[i]) > 0:
            _recent_outliers += np.sum(distance_buckets[i] > mean[i] + alpha * std[i])
        else:
            print(f"Cluster {i}: No data in this cluster")

    OR = compute_or([_recent_outliers, _historical_outliers], [_recent_samples, _historical_samples])

    log_K.append(K)
    log_OR.append(OR)

    print(f'## K = {K}, Alpha = {alpha}, {_recent_outliers}/{_recent_samples}, {_historical_outliers}/{_historical_samples}, OR = {OR}')
    return OR, _historical_outliers


if __name__ == '__main__':
    for i in range(50):
        alpha = round(0.0 + i * 0.05, 2)
        OR, outliers = do_loop(5, alpha)

        if outliers < 500:
            break

        with open(f'txt/alpha_or/output_alpha.txt', 'a') as f:
            f.write(f"{alpha},")

        with open(f'txt/alpha_or/output_or.txt', 'a') as f:
            f.write(f"{OR},")

        with open(f'txt/alpha_or/output_outliers.txt', 'a') as f:
            f.write(f"{outliers},")

