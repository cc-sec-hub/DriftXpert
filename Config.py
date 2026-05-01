# !/usr/bin/env python3


batch_size = 256

cic_feature_num = 50
cic_hiddens1 = 96
cic_hiddens2 = 64
cic_output1 = 32
cic_output2 = 2

label_names = ['Benign', 'FTP-Patator', 'SSH-Patator', 'DoS-GoldenEye',
          'DoS-Hulk', 'DoS-Slowloris', 'DoS-SlowHttpTest', 'Bot', 'Web-BruteForce']

local_drift_set1_path = '../IntrusionDetection/DriftXpert/Dataset/data/CICIDS-2017-LocalDrift-1.csv'
local_drift_set2_path = '../IntrusionDetection/DriftXpert/Dataset/data/CICIDS-2017-LocalDrift-2.csv'

l0main_set1_model_path = [
    'pkl/l0main/l0model-1.pkl',
    'pkl/l0main/l0encoder-1.pkl',
    'pkl/l0main/l0cls-1.pkl',
]

l0main_set2_model_path = [
    'pkl/l0main/l0model-2.pkl',
    'pkl/l0main/l0encoder-2.pkl',
    'pkl/l0main/l0cls-2.pkl',
]

l1main_model_path = [
    'pkl/l1main/l1model.pkl',
    'pkl/l1main/l1encoder.pkl',
    'pkl/l1main/l1cls.pkl',
]

l1_freeze_ec_path = [
    'pkl/l1_freeze_ec/l1model.pkl',
    'pkl/l1_freeze_ec/l1encoder.pkl',
    'pkl/l1_freeze_ec/l1cls.pkl',
]

l1_not_freeze_model_path = [
    'pkl/l1_not_freeze/l1model.pkl',
    'pkl/l1_not_freeze/l1encoder.pkl',
    'pkl/l1_not_freeze/l1cls.pkl',
]

l1_ft_model_path = [
    'pkl/l1_ft/l1model.pkl',
    'pkl/l1_ft/l1encoder.pkl',
    'pkl/l1_ft/l1cls.pkl',
]

l1_ft_freeze_layer_model_path = [
    'pkl/l1_ft_freeze_layer/l1model.pkl',
    'pkl/l1_ft_freeze_layer/l1encoder.pkl',
    'pkl/l1_ft_freeze_layer/l1cls.pkl',
]

l1_not_aggregation_path = [
    'pkl/l1_not_aggregation/l1model.pkl',
    'pkl/l1_not_aggregation/l1encoder.pkl',
    'pkl/l1_not_aggregation/l1cls.pkl',
]

column_names = ['Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
       'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
       'Fwd Packet Length Max', 'Fwd Packet Length Min',
       'Fwd Packet Length Mean', 'Fwd Packet Length Std',
       'Bwd Packet Length Max', 'Bwd Packet Length Min',
       'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s',
       'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
       'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std',
       'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
       'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags',
       'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s',
       'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
       'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
       'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
       'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
       'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
       'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward',
       'Label']