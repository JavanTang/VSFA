'''
@Author: TangZhiFeng
@Data: Do not edit
@LastEditors: TangZhiFeng
@LastEditTime: 2020-03-24 10:42:07
@Description: 测试算法的准确度
'''

# 下载所有清晰视频
import pandas as pd
from utils import download_mp4, get_dir_all_file
from test_demo import predict
clear_data = pd.read_csv('clear.csv', sep=',')
url_pre = clear_data['url_pre'][0]
clear_data =url_pre + clear_data['video_key']
download_mp4(clear_data, 'clear_videos/')


blur_data = pd.read_csv('blur.csv', sep=',')
url_pre = blur_data['url_pre'][0]
blur_data =url_pre + blur_data['video_key']
download_mp4(blur_data, 'blur_videos/')


# 评测clear视频
clear_score = {}
clear_videos = get_dir_all_file('clear_videos/', suffix=['mp4'])
for i in clear_videos:
    clear_score[i] = predict(i)


# 评测blur视频
blur_score = {}
blur_videos = get_dir_all_file('blur_videos/', suffix=['mp4'])
for i in blur_videos:
    blur_score[i] = predict(i)

