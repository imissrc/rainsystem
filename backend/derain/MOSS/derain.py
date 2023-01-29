import os.path
import torch
import math
import torch.nn.functional as F
from torch.autograd import Variable

import torchvision.transforms as transforms
from pathlib import Path

from backend.derain.MOSS.dataset import *

try:
    from ruamel import yaml
except:
    import yaml
from easydict import EasyDict as edict

from backend.derain.MOSS.networks import NetG
import torchvision.utils as vutils

str_to_list = lambda x: [int(xi) for xi in x.split(',')]


def loadModel():

    cur_path = Path(__file__).resolve().parent

    config = {}

    with open(os.path.join(cur_path, "test.yaml"), 'r') as stream:
        config = edict(yaml.load(stream, Loader=yaml.FullLoader))


    model = NetG(config).cuda()

    state = torch.load(os.path.join(cur_path,'ddn_ssir.pth'))
    model.load_state_dict(state)
    model.eval()

    return model


def derainReal(model, input_image_data_list):
    normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])

    output_image_list = []
    with torch.no_grad():
        for image_data in input_image_data_list:
            data = dealSingleImage(image_data, normalize)
            if len(data.size()) == 3:
                data = data.unsqueeze(0)
            data = Variable(data).cuda()
            _, c, h, w = data.size()
            h1 = math.ceil(h / 8.) * 8
            w1 = math.ceil(w / 8.) * 8
            if h1 != h or w1 != w:
                data = F.interpolate(data, (h1, w1), mode='bicubic')

            fake = model(data)
            if h1 != h or w1 != w:
                fake = F.interpolate(fake, (h, w), mode='bicubic')
            output_image_list.append(imageTensorToNumpy(fake * 0.5 + 0.5))

    return output_image_list

def imageTensorToNumpy(tensor):
    grid = vutils.make_grid(tensor)
    # Add 0.5 after unnormalizing to [0, 255] to round to nearest integer
    img = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to('cpu', torch.uint8).numpy()
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
