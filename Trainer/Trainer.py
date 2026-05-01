import time
import copy
import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from torch import nn
from torch.autograd import Variable
from Models.Models import IDS, LoadIDS
from Trainer.ContrastiveLoss import ContrastiveLoss
from Config import *
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 设置字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
font = FontProperties(fname=font_path, size=16)


class Trainer():
    def __init__(self, lr, epoch, cuda, device) -> None:
        self.__lr = lr
        self.__epoch = epoch
        self.__cuda = cuda
        self.__device = device
        self.__ctt_loss = []


    def L0Train(self, train_loader, model_path, encoder_path, cls_path):
        start = time.time()

        model = IDS(cic_feature_num, cic_hiddens1, cic_hiddens2, \
            cic_output1, cic_output2).to(self.__device)
        
        optimizer = torch.optim.Adam(model.parameters(), lr=self.__lr)
        ce_func = nn.CrossEntropyLoss()

        model.train()

        for epoch in range(self.__epoch):
            train_loss = 0
            for (X, labels) in train_loader:
                X = Variable(X.float())
                labels = Variable(labels.long())
                if self.__cuda: 
                    X = X.cuda()
                    labels = labels.cuda()

                preds, _ = model(X)
                
                _labels = torch.zeros(len(labels), cic_output2).to(self.__device)
                _labels = _labels.scatter_(1, labels.unsqueeze(1), 1)

                loss = ce_func(preds, _labels)
            
                optimizer.zero_grad()
                loss.backward()
                train_loss += loss.item()
                optimizer.step()

            print('Epoch [%d/%d] Loss: %.4f' % (epoch + 1, 
                        self.__epoch, train_loss / len(train_loader)))

        torch.save(model, model_path)
        torch.save(model.encoder, encoder_path)
        torch.save(model.dense, cls_path)
        
        end = time.time()
        run_time = end - start
        print('run time: %.2fs.' % run_time)


    def Test(self, test_loader, set_type, model_path, smt_path : str=None):
        _model = torch.load(model_path).to(self.__device)
        _model.eval()  
        
        total, correct = 0, 0
        index = 0
        _pred_dists = None
        
        for (X_test, labels) in test_loader:
            X_test = Variable(X_test.float())
            labels = Variable(labels.long())
            if self.__cuda:
                X_test = X_test.cuda()
                labels = labels.cuda()

            y, _smt = _model(X_test)
            
            _p = nn.functional.softmax(y, dim=1)
            predict = torch.argmax(_p, axis=1)

            total += X_test.size(0)
            correct += (predict == labels).sum()

            if index == 0:
                ret = predict.cpu().data
                smts = torch.cat([_smt.cpu().data, labels.reshape(-1, 1).cpu().data], dim=1)
                _pred_dists = torch.cat([_p.cpu().data, labels.reshape(-1, 1).cpu().data, 
                                         predict.reshape(-1, 1).cpu().data], dim=1)
            else:
                ret = torch.cat((ret, predict.cpu().data), axis=0)
                smt = torch.cat([_smt.cpu().data, labels.reshape(-1, 1).cpu().data], dim=1)
                smts = torch.cat([smts, smt], dim=0)
                _pred_dist = torch.cat([_p.cpu().data, labels.reshape(-1, 1).cpu().data, 
                                        predict.reshape(-1, 1).cpu().data], dim=1)
                _pred_dists = torch.cat([_pred_dists, _pred_dist], dim=0)

            index = index + 1

        if smt_path is not None:
            smts = pd.DataFrame(smts.numpy())
            smts.to_csv(smt_path, index=None)

        _pred_dists = pd.DataFrame(_pred_dists.numpy(), columns=['P1', 'P2', 'Label', 'Pred'])
        self.__plot_dist(_pred_dists[(_pred_dists.Label == 0) & (_pred_dists.Pred == 0)], f'./jpg/{set_type}_pred_dists_00.jpg')
        self.__plot_dist(_pred_dists[(_pred_dists.Label == 0) & (_pred_dists.Pred == 1)], f'./jpg/{set_type}_pred_dists_01.jpg')
        self.__plot_dist(_pred_dists[(_pred_dists.Label == 1) & (_pred_dists.Pred == 0)], f'./jpg/{set_type}_pred_dists_10.jpg')
        self.__plot_dist(_pred_dists[(_pred_dists.Label == 1) & (_pred_dists.Pred == 1)], f'./jpg/{set_type}_pred_dists_11.jpg')

        print('Test Accuracy of the model on the %s set: %4f %%' 
                % (set_type, 100.0 * correct / total))
        return ret
    

    def __plot_dist(self, data, save_path):
        # 创建绘图对象
        plt.figure(figsize=(10, 6))

        sns.kdeplot(data=data, x='P1', color='blue', label='Benign', fill=False)
        sns.kdeplot(data=data, x='P2', color='red', label='Attack', fill=False)

        plt.xlabel('Value')
        plt.ylabel('Density')

        plt.legend()
        plt.savefig(save_path, dpi=256)
        plt.close()
    

    def __plot_ctt_loss(self, save_path):
        plt.figure(figsize=(8, 6))  # 设置图像大小
        epochs = [i for i in range(1, len(self.__ctt_loss) + 1)]
        plt.plot(epochs, self.__ctt_loss, marker='', markersize=0, linestyle='-', linewidth=1, color='b')

        plt.xlabel('Epoch', font=font)
        plt.ylabel('Loss', font=font)

        epochs = [i * 50 for i in range(0, int(len(self.__ctt_loss) / 50 + 1))]
        plt.xticks(epochs, font=font)
        plt.yticks(font=font)
        plt.grid(True, linestyle='--', alpha=0.6)
        
        plt.tight_layout()

        # 显示图表
        plt.savefig(save_path)

    
    # 打印模型参数
    def model_state_dict(self, model_path):
        model = torch.load(model_path).to(self.__device)
        model.eval() 

        for name, param in model.state_dict().items():
            if 'dense1.weight' in name:
                print(f"{name}: {param.shape}\n{param[:1,:10]}")
