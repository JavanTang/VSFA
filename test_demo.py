'''
@Author: TangZhiFeng
@Data: Do not edit
@LastEditors: TangZhiFeng
@LastEditTime: 2020-03-24 10:04:11
@Description: 预测质量模块
'''
"""Test Demo for Quality Assessment of In-the-Wild Videos, ACM MM 2019"""
#
# Author: Dingquan Li
# Email: dingquanli AT pku DOT edu DOT cn
# Date: 2018/3/27
#
import torch
from torchvision import transforms
import skvideo.io
from PIL import Image
import numpy as np
from VSFA import VSFA
from CNNfeatures import get_features
import time

def predict(video_path, model_path='models/VSFA.pt', video_format='RGB', video_width=None, video_height=None,
            frame_batch_size=16):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # data preparation
    assert video_format == 'YUV420' or video_format == 'RGB'
    if video_format == 'YUV420':
        video_data = skvideo.io.vread(video_path, video_height, video_width, inputdict={'-pix_fmt': 'yuvj420p'})
    else:
        video_data = skvideo.io.vread(video_path)
    video_length = video_data.shape[0]
    video_channel = video_data.shape[3]
    video_height = video_data.shape[1]
    video_width = video_data.shape[2]
    transformed_video = torch.zeros([video_length, video_channel, video_height, video_width])
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    for frame_idx in range(video_length):
        frame = video_data[frame_idx]
        frame = Image.fromarray(frame)
        frame = transform(frame)
        transformed_video[frame_idx] = frame

    print('Video length: {}'.format(transformed_video.shape[0]))

    # feature extraction
    features = get_features(transformed_video, frame_batch_size=frame_batch_size, device=device)
    features = torch.unsqueeze(features, 0)  # batch size 1

    # quality prediction using VSFA
    model = VSFA()
    model.load_state_dict(torch.load(model_path))  #
    model.to(device)
    model.eval()
    with torch.no_grad():
        input_length = features.shape[1] * torch.ones(1, 1)
        outputs = model(features, input_length)
        y_pred = outputs[0][0].to('cpu').numpy()
        return y_pred
