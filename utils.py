'''
@Author: TangZhiFeng
@Data: Do not edit
@LastEditors: TangZhiFeng
@LastEditTime: 2020-03-24 10:43:11
@Description: 工具类
'''


import os
import cv2


__all__ = ['obtain_frame', 'get_dir_all_file', 'download_mp4']
def get_dir_all_file(dir_path, suffix = None):
    """获取dir_path下面所有文件
    
    Arguments:
        dir_path {str} -- 文件夹位置
    
    Keyword Arguments:
        suffix {list} -- 要求的后缀,例如['png','jpeg'] (default: {None})
    
    Returns:
        list -- 文件夹下的文件list
    """
    files = []
    for _dir,_,_files in os.walk(dir_path):
        for i in _files:
            _i = i.split('.')
            if len(_i) < 2: continue
            _suffix = _i[-1]
            if suffix is not None:
                if _suffix in suffix:
                    files.append(os.path.join(dir_path, i))
            else:
                files.append(os.path.join(dir_path, i))
    return files

def obtain_frame(video_path):
    #视频帧率12
    fps = 30
    #保存图片的帧率间隔
    count = 60
    #开始读视频
    try:
        videoCapture = cv2.VideoCapture(video_path)
        i = 0
        j = 0
        savedpath = 'images/'
        images = []
        while True:
            success,frame = videoCapture.read()
            i+=1
            if(i % count ==0):
                #保存图片
                j += 1
                savedname = video_path.split('/')[-1].split('.')[0] + '_' + str(j) + '_' + str(i)+'.jpg'
                img_path = savedpath + savedname
                cv2.imwrite(img_path ,frame)
                images.append(img_path)
                print('image of %s is saved'%(img_path))
            if not success:
                print('video is all read')
                break
        except Exception as e:
            print('video_path:' ,video_path)
            print('读取视频出错!')
            images = None
    return images

def download_mp4(urls, dir_path='./videos'):
    for i in urls:
        os.system("wget -P %s %s" % (dir_path, i))
        file_name = os.path.join(dir_path, i.split('/')[-1])
        new_path = os.path.join(dir_path, file_name.split('/')[-1].split('.')[0] + '_new.mp4')
        os.system("ffmpeg -ss 00:00:00 -t 00:00:5 -i %s -vcodec copy -acodec copy %s" % (file_name, new_path))
        os.system("rm %s" % (file_name))

if __name__ == "__main__":
    # print(get_dir_all_file('data', suffix=['png', 'jpeg']))
    pass