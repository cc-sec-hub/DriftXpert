import torch
import pandas as pd
import numpy as np
import torch.utils.data as Data
from sklearn import preprocessing
from sklearn.model_selection import train_test_split


class DataSets:
    def __init__(self):
        pass
    

    def LoadDataset(self, path, test_size=0.0):
        df = pd.read_csv(path).sample(frac=1.0)

        data = np.array(df)
        label_pos = data.shape[1] - 1
        X = data[:,:label_pos]  
        y = data[:,label_pos]

        if test_size != 0.0:
            X1, X2, y1, y2 = train_test_split(X, y, test_size=test_size, random_state=42)
            # pd.df & np to torch.tensor
            return torch.from_numpy(X1), torch.from_numpy(X2), \
                torch.from_numpy(y1), torch.from_numpy(y2)
        return torch.from_numpy(X), torch.from_numpy(y)
    

    def LoadDataloader(self, X, y, batch_size):
        dataset = Data.TensorDataset(X, y)
        data_loader = Data.DataLoader(dataset=dataset, batch_size=batch_size, 
                shuffle=False, num_workers=4)
        return data_loader
    