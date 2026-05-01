import torch
import numpy as np
import sklearn
from Config import *
from Trainer.Datasets import DataSets
from Trainer.Trainer import Trainer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

print(torch.__version__)
print(np.__version__)
print(sklearn.__version__)


def cls_report(y, preds, title):
    report = classification_report(y, preds, digits=4)
    print(title)
    print(report)


if __name__ == '__main__':
    torch.manual_seed(1234)

    batch_size = 256
    learning_rate = 1e-4
    epoch = 100
    
    no_cuda = True
    cuda_available = not no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if cuda_available else "cpu")

    _data = DataSets()
    _trainer = Trainer(learning_rate, epoch, cuda_available, device)

    _train_no = 2

    if _train_no == 1:
        set1_path = local_drift_set1_path
        set2_path = local_drift_set2_path
        model_path = l0main_set1_model_path
    else:
        set1_path = local_drift_set2_path
        set2_path = local_drift_set1_path
        model_path = l0main_set2_model_path

    TrainX, TestX, TrainY, TestY = _data.LoadDataset(set1_path, test_size=0.2)
    TrainDataloader = _data.LoadDataloader(TrainX, TrainY, batch_size)
    _trainer.L0Train(TrainDataloader, model_path[0], model_path[1], model_path[2])

    TestDataloader = _data.LoadDataloader(TestX, TestY, batch_size * 5)
    preds = _trainer.Test(TestDataloader, f'l0_main_test_{_train_no}', model_path[0], 
                          smt_path='csv/l0/historical_data_smts.csv')
    cls_report(TestY, preds, f'## l0_main_test_{_train_no}:')

    TestX, TestY = _data.LoadDataset(set2_path)
    TestDataloader = _data.LoadDataloader(TestX, TestY, batch_size * 5)
    preds = _trainer.Test(TestDataloader, f'l0_main_test_{3 - _train_no}', model_path[0], 
                          smt_path='csv/l0/drift_data_smts.csv')
    cls_report(TestY, preds, f'## l0_main_test_{3 - _train_no}:')

