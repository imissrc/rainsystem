from PIL import Image, ImageOps
import random
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF
import cv2
import numpy as np

def load_single_image(image_data, input_height=128, input_width=None, output_height=128, output_width=None,
              crop_height=None, crop_width=None, is_random_crop=True, is_gray=False, random_scale=None):

    if input_width is None:
      input_width = input_height
    if output_width is None:
      output_width = output_height
    if crop_width is None:
      crop_width = crop_height

    img = Image.fromarray(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))
    # img = Image.fromarray(np.uint8(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)))

    if is_gray is False and img.mode is not 'RGB':
      img = img.convert('RGB')
    if is_gray and img.mode is not 'L':
      img = img.convert('L')

    if random_scale is not None:
        if random.random() < 0.5:
            [w, h] = img.size
            ww = random.randint(int(w*random_scale), w)
            hh = random.randint(int(h*random_scale), h)
            img = img.resize((ww, hh), Image.BICUBIC)
      

    if input_height is not None:
      img = img.resize((input_width, input_height),Image.BICUBIC)
      
    [w, h] = img.size
    if crop_height is not None:      
      if is_random_crop:
        #print([w,cropSize])
        if crop_width < w:
            cx1 = random.randint(0, w-crop_width)
            cx2 = w - crop_width - cx1
        else:
            cx1, cx2 = 0, 0
        if crop_height < h:
            cy1 = random.randint(0, h-crop_height) 
            cy2 = h - crop_height - cy1
        else:
            cy1, cy2 = 0, 0
      else:
        if crop_width < w:
            cx2 = cx1 = int(round((w-crop_width)/2.))
        else:
            cx2 = cx1 = 0
        if crop_height < h:
            cy2 = cy1 = int(round((h-crop_height)/2.))
        else:
            cy2 = cy1 = 0
      img = ImageOps.crop(img, (cx1, cy1, cx2, cy2))      
    if output_height is not None:
        img = img.resize((output_width, output_height),Image.BICUBIC)
    return img

def dealSingleImage(image_data, normalize=None):
        height, width, _ = image_data.shape
        img = load_single_image(image_data, height, width, height, width)
        if normalize is None:
            transform = transforms.Compose([transforms.ToTensor()])
        else:
            transform = transforms.Compose([transforms.ToTensor(), normalize])

        img = transform(img)

        return img