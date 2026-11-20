import torch
import numpy as np
from Config import *
from Trainer.Datasets import DataSets
from Trainer.Trainer import Trainer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


def cls_report(y, preds, title):
    report = classification_report(y, preds, digits=4)
    print(title)
    print(report)


if __name__ == '__main__':
    torch.manual_seed(1234)

    batch_size = 256
    learning_rate = 1e-3
    epoch = 5
    
    no_cuda = True
    cuda_available = not no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if cuda_available else "cpu")

    _data = DataSets()
    _trainer = Trainer(learning_rate, epoch, cuda_available, device)

    TrainX, TestX, TrainY, TestY = _data.LoadDataset(global_drift_set2_path, test_size=0.2)
    TrainDataloader = _data.LoadDataloader(TrainX, TrainY, batch_size)
    _trainer.L1TrainFT(l0main_set1_model_path[0], TrainDataloader, l1_ft_model_path[0], freeze_layer=False)

    TestDataloader = _data.LoadDataloader(TestX, TestY, batch_size * 5)
    preds = _trainer.Test(TestDataloader, 'l1_main_test_2', l1_ft_model_path[0])
    cls_report(TestY, preds, f'## l1_main_test_2:')

    TestX, TestY = _data.LoadDataset(global_drift_set1_path)
    TestDataloader = _data.LoadDataloader(TestX, TestY, batch_size * 5)
    preds = _trainer.Test(TestDataloader, 'l1_main_test_1', l1_ft_model_path[0])
    cls_report(TestY, preds, f'## l1_main_test_1:')
