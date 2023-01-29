import torch
import torch.nn.functional as F
# import torchvision.transforms.functional as TF
# from PIL import Image
from skimage import img_as_ubyte
import numpy as np

def derain(model, input_image_list):
    output_image_list = []
    for input_image in input_image_list:
        if input_image.any() == None:
            exit()

        img_multiple_of = 8

        # img = Image.open(input_image).convert('RGB')
        # input_ = TF.to_tensor(img).unsqueeze(0).cuda()
        input_ = np.float32(input_image) / 255.0
        input_ = input_.transpose((2, 0, 1))
        input_ = torch.from_numpy(input_).unsqueeze(0).cuda()

        # Pad the input if not_multiple_of 8
        h, w = input_.shape[2], input_.shape[3]
        H, W = ((h + img_multiple_of) // img_multiple_of) * img_multiple_of, (
                    (w + img_multiple_of) // img_multiple_of) * img_multiple_of
        padh = H - h if h % img_multiple_of != 0 else 0
        padw = W - w if w % img_multiple_of != 0 else 0
        input_ = F.pad(input_, (0, padw, 0, padh), 'reflect')

        with torch.no_grad():
            restored = model(input_)
        restored = restored[0]
        # 将输入input张量每个元素的夹紧到区间 [min,max][min,max]，并返回结果到一个新张量。
        restored = torch.clamp(restored, 0, 1)

        # Unpad the output
        restored = restored[:, :, :h, :w]

        restored = restored.permute(0, 2, 3, 1).cpu().detach().numpy()
        restored = img_as_ubyte(restored[0])
        output_image_list.append(restored)

    return output_image_list

