import cv2
import os
import numpy as np

def imagesToVideo(images, fps, file_path):
    if len(images) == 0:
        raise Exception("image list size is 0")
    # 高， 宽， 通道数
    image_shape = images[0].shape
    file_path = file_path.replace(file_path.split('.')[-1], 'avi')
    size = (image_shape[1], image_shape[0])  # 需要转为视频的图片的尺寸
    video = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), fps, size)  # avi格式

    for i in range(len(images)):
        video.write(images[i])
    video.release()
    cv2.destroyAllWindows()


def videoToImages(video_path):
    cap = cv2.VideoCapture(video_path)  # 获取到一个视频
    images = list()
    while cap.isOpened():
        (flag, frame) = cap.read()  # 读取一张图像
        if (flag == True):
            # 设置保存路径
            images.append(frame)
        else:
            break
    fps = cap.get(cv2.CAP_PROP_FPS)
    return images, fps


def videoMerge(video1, video2, fps, file_path):#两个图片列表合并为一个视频
    merged = list()
    print(type(video1[0]))
    print(type(video2[0]))
    for img1, img2 in zip(video1, video2):
        merged.append(np.hstack((img1, img2)))
    imagesToVideo(merged, fps, file_path)


'''
将图片转化为avi视频
'''
def convertImagesToAVI(data_path, fps, out_file, ext):
    files = os.listdir(data_path)
    files = [x for x in files if x.endswith(ext)]
    new_files = sorted(files, key=lambda x: int(x[:-1 * len(ext)]))
    image = cv2.imread(os.path.join(data_path, new_files[0]))
    # 高， 宽， 通道数
    image_shape = image.shape


def mp4ToAvi(input_path, output_path):
    cap = cv2.VideoCapture(input_path)  # 获取到一个视频
    images = list()
    while cap.isOpened():
        (flag, frame) = cap.read()  # 读取一张图像
        if (flag == True):
            # 设置保存路径
            images.append(frame)
        else:
            break
    fps = cap.get(cv2.CAP_PROP_FPS)
    image_shape = images[0].shape
    size = (image_shape[1], image_shape[0])  # 需要转为视频的图片的尺寸
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, size)  # avi格式

    for i in range(len(images)):
        video.write(images[i])
    video.release()
    cv2.destroyAllWindows()


def convertImagesToMp4(data_path, fps, out_file, ext):
    files = os.listdir(data_path)
    files = [x for x in files if x.endswith(ext)]
    new_files = sorted(files, key=lambda x: int(x[:-1 * len(ext)]))
    image = cv2.imread(os.path.join(data_path, new_files[0]))
    # 高， 宽， 通道数
    image_shape = image.shape
    size = (image_shape[1], image_shape[0])  # 需要转为视频的图片的尺寸
    video = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for i in range(len(new_files)):
        image_path = os.path.join(data_path, new_files[i])
        img = cv2.imread(image_path)
        video.write(img)

    video.release()
    cv2.destroyAllWindows()

'''
    将avi视频转化为图片
    '''

def convertVideoToImages(video_file, target_dir):
    cap = cv2.VideoCapture(video_file)  # 获取到一个视频
    isOpened = cap.isOpened  # 判断是否打开
    i = 0
    while isOpened:
        i += 1
        (flag, frame) = cap.read()  # 读取一张图像

        fileName = str(i) + ".png"
        if (flag == True):
            # 设置保存路径
            save_path = os.path.join(target_dir, fileName)
            if not cv2.imwrite(save_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100]):
                raise Exception("Could not write image")
        else:
            break


