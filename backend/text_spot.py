#!/usr/local/bin/python3
"""
@Project : rainsystem
@File    : text_spot.py
@Author  : Ray
@Time    : 2021/11/23 14:40
"""
import backend.ImageVideo as imageVideo
import time


def get_video_ocr(model, input_video_path, output_video_path):
    if input_video_path == '':
        return
    output_video_images, fps = run_video_ocr_model(model, input_video_path)
    imageVideo.imagesToVideo(output_video_images, fps, output_video_path)


def get_img_list_ocr(model, image_list):
    output = list()
    for img in image_list:
        _, res_img = model.readtext_for_video(img=img)
        if isinstance(res_img, list):
            for i in range(len(res_img)):
                output.append(res_img[i])
        else:
            output.append(res_img)
    return output


def run_video_ocr_model(model, input_video_path):
    # 输入视频路径，将视频拆分成图片，对图片进行文字识别
    input_video_image_list, fps = imageVideo.videoToImages(input_video_path)

    start = time.time()
    print(input_video_path)
    print(len(input_video_image_list))
    output_video_images = []
    for video_image in input_video_image_list:
        # 要判断返回的是不是list，判断 list 长度
        _, output_image = model.readtext_for_video(img=video_image)
        # print("run_video_ocr_model() 的image长度是：")
        # print(len(output_image))  # list()
        # print("run_video_ocr_model() 的output_image[0]的数据类型：")
        # print(type(output_image[0]))
        if isinstance(output_image, tuple):
            print(output_image[0])
            print(output_image[1])
            raise RuntimeError("模型输出的image类型是tuple")
        if isinstance(output_image, list):
            for i in range(len(output_image)):
                output_video_images.append(output_image[i])
        else:
            output_video_images.append(output_image)

    print("end")
    print("time: " + str(time.time() - start))
    # output_video_images 应该是 list of np.ndarray
    return output_video_images, fps

