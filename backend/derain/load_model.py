from runpy import run_path
import os
from pathlib import Path
import torch
from collections import OrderedDict
import backend.derain.MOSS.derain as MossDerain

def createMprnet():
    cur_path = Path(__file__).resolve().parent
    # Load corresponding dao architecture and weights
    load_file = run_path(os.path.join(cur_path, "MPRNet/MPRNet.py"))
    model = load_file['MPRNet']()
    model.cuda()

    weights = os.path.join(os.path.join(cur_path, "MPRNet/pretrained_models", "model_best" + ".pth"))
    load_mprnet_checkpoint(model, weights)
    model.eval()
    return model

def load_mprnet_checkpoint(model, weights):
    checkpoint = torch.load(weights, map_location='cpu')
    try:
        model.load_state_dict(checkpoint["state_dict"])
    except:
        state_dict = checkpoint["state_dict"]
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:] # remove `module.`
            new_state_dict[name] = v
        model.load_state_dict(new_state_dict)

def createMoss():

    return MossDerain.loadModel()