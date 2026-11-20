import torch
import torch.nn as nn
import torch.nn.functional as F


class ContrastiveLoss(nn.Module):
    def __init__(self, temperature=1.0):
        """
        对比损失模块初始化

        参数:
            temperature (float): 温度系数 τ，控制相似性缩放
        """
        super(ContrastiveLoss, self).__init__()
        self.temperature = temperature


    def forward(self, z, z_old, z_prev):
        """
        计算对比损失

        参数:
            z (torch.Tensor): 当前样本的嵌入向量 (batch_size, dim)
            z_glob (torch.Tensor): 全局嵌入向量 (batch_size, dim)
            z_prev (torch.Tensor): 先前嵌入向量 (batch_size, dim)

        返回:
            torch.Tensor: 损失标量
        """
        # 确保向量归一化
        z = F.normalize(z, p=2, dim=-1)
        z_old = F.normalize(z_old, p=2, dim=-1)
        z_prev = F.normalize(z_prev, p=2, dim=-1)

        # 计算相似性（余弦相似性）
        sim_z_zold = F.cosine_similarity(z, z_old, dim=-1)
        sim_z_zprev = F.cosine_similarity(z, z_prev, dim=-1)

        # 计算 exp(similarity / temperature)
        exp_sim_z_zold = torch.exp(sim_z_zold / self.temperature)
        exp_sim_z_zprev = torch.exp(sim_z_zprev / self.temperature)

        # 分母: exp(sim(z, z_glob)/τ) + exp(sim(z, z_prev)/τ)
        denominator = exp_sim_z_zold + exp_sim_z_zprev

        # 对比损失: -log(exp(sim(z, z_glob)/τ) / denominator)
        loss = -torch.log(exp_sim_z_zold / denominator)

        # 返回平均损失
        return loss.mean()
