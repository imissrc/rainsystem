from pathlib import Path
import time
import backend.derain.MPRNet.derain as derain
import backend.derain.MOSS.derain as mossDerain
# 要选择的模型名称，输入图片的绝对路径
import backend.ImageVideo as imageVideo
import cv2

def getVideoDerainImages(model, input_video_path, model_name='moss'):
    return runVideoDerainModel(model, input_video_path, model_name)

def getVideoDerain(model, input_video_path, output_video_path, model_name='moss'):
    if input_video_path == '':
        return
    input_video_images, output_video_images, fps = runVideoDerainModel(model, input_video_path, model_name)
    imageVideo.videoMerge(input_video_images, output_video_images, fps, output_video_path)
    # imageVideo.imagesToVideo(output_video_images, fps, output_video_path)

def getImageDerain(model, input_path, output_path, model_name='moss'):
    input_image = cv2.imread(input_path)
    output_image = runImageDerainModel(model, input_image, model_name)
    cv2.imwrite(output_path, output_image)

def runImageDerainModel(model, input_image, model_name='moss'):
    output_image_list = []
    if model_name == 'mprnet':
        output_image_list = derain.derain(model, [input_image])
    elif model_name == 'moss':
        output_image_list = mossDerain.derainReal(model, [input_image])
    if len(output_image_list) > 0:
        return output_image_list[0]
    return None

def runVideoDerainModel(model, input_video_path, model_name='moss'):
    input_video_images, fps = imageVideo.videoToImages(input_video_path)

    start = time.time()
    output_video_images = []
    if model_name == 'mprnet':
        output_video_images = derain.derain(model, input_video_images)
    elif model_name == 'moss':
        output_video_images = mossDerain.derainReal(model, input_video_images)
        output_video_images = mossDerain.derainReal(model, output_video_images)
        output_video_images = mossDerain.derainReal(model, output_video_images)
        output_video_images = mossDerain.derainReal(model, output_video_images)

    print("end")
    print("time: " + str(time.time() - start))
    return input_video_images, output_video_images, fps


