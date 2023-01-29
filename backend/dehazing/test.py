import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.utils as vutils
from backend.dehazing.models.FFA import FFANet
from backend.dehazing.models.GCA import GCANet
from backend.ImageVideo import imagesToVideo, videoToImages, videoMerge
import numpy as np
import os
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Normalize
import datetime

def edge_compute(x):
    x_diffx = torch.abs(x[:,:,1:] - x[:,:,:-1])
    x_diffy = torch.abs(x[:,1:,:] - x[:,:-1,:])

    y = x.new(x.size())
    y.fill_(0)
    y[:,:,1:] += x_diffx
    y[:,:,:-1] += x_diffx
    y[:,1:,:] += x_diffy
    y[:,:-1,:] += x_diffy
    y = torch.sum(y,0,keepdim=True)/3
    y /= 4
    return y

def create_dehazingModel():
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    #device_ids = [2]
    #device = torch.device("cuda:2")
    #net = GCANet(in_c=4, out_c=3, only_residual=True)#.to(device)
    net = FFANet(3, 19)
    # net = MSBDNNet()
    #net = nn.DataParallel(net, device_ids=device_ids)
    net = nn.DataParallel(net)
    os.path.abspath('.')
    #net.load_state_dict(torch.load(os.path.abspath('.') + '/backend/dehazing/PSD-GCANET', map_location=str(torch.device('cuda:2'))))
    net.load_state_dict(
        torch.load(os.path.abspath('.') + '/backend/dehazing/PSD-FFANET'))
    # net.load_state_dict(torch.load('PSB-MSBDN'))

    net.eval()
    return net
    # test_data_loader = DataLoader(TestData_GCA(test_data_dir), batch_size=1, shuffle=False, num_workers=8) # For GCA
    #test_data_loader = DataLoader(TestData_FFA(test_data_dir), batch_size=1, shuffle=False, num_workers=8) # For FFA and MSBDN

def run_dehazingmodel(model, haze_image, type=0):
    
    with torch.no_grad():
        if type == 0:
            haze_reshaped = haze_image
            haze_reshaped = haze_reshaped.resize((512, 512), Image.ANTIALIAS)
            transform_haze = Compose([ToTensor(), Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
            haze = transform_haze(haze_image).unsqueeze_(0)
            haze_reshaped = transform_haze(haze_reshaped)
            pred = model(haze, haze_reshaped, True)
            ts = torch.squeeze(pred.clamp(0, 1).cpu()) * 255
            out_img = Image.fromarray(ts.numpy().astype(np.uint8).transpose(1, 2, 0))
            return out_img
        elif type == 1:
            for i in range(len(haze_image)):
                haze_reshaped = haze_image[i]
                haze_reshaped = haze_reshaped.resize((512, 512), Image.ANTIALIAS)
                transform_haze = Compose([ToTensor(), Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
                haze = transform_haze(haze_image[i]).unsqueeze_(0)
                haze_reshaped = transform_haze(haze_reshaped)
                if i == 0:
                    hazes = haze
                    hazes_reshaped = haze_reshaped
                else:
                    hazes = torch.cat((hazes, haze), dim=0)
                    hazes_reshaped = torch.cat((hazes_reshaped, haze_reshaped), dim=0)
            pred = model(hazes, hazes_reshaped, True)
            preds = torch.split(pred, 1, dim=0)
            out_imgs = list()
            for img in preds:
                ts = torch.squeeze(img.clamp(0, 1).cpu()) * 255
                out_img = ts.numpy().astype(np.uint8).transpose(1, 2, 0)
                out_imgs.append(out_img)
            return out_imgs
        # if type == 0:
        #     im_w, im_h = haze_image.size
        #     if im_w % 4 != 0 or im_h % 4 != 0:
        #         haze_image = haze_image.resize((int(im_w // 4 * 4), int(im_h // 4 * 4)))
        #     img = np.array(haze_image).astype('float')
        #     img = torch.from_numpy(img.transpose((2, 0, 1))).float()
        #     edge = edge_compute(img)
        #     haze = torch.cat((img, edge), dim = 0) - 128
        #     haze = haze.unsqueeze_(0)
        #     pred = model(haze, 0, True, False)
        #     dehaze = pred.float().round().clamp(0, 255)
        #     out_img = Image.fromarray(dehaze[0].cpu().numpy().astype(np.uint8).transpose(1, 2, 0))
        #     return out_img
        # elif type == 1:
        #     im_w, im_h = haze_image[0].size
        #     if im_w % 4 != 0 or im_h % 4 != 0:
        #         for i in range(len(haze_image)):
        #             haze_image[i] = haze_image[i].resize((int(im_w // 4 * 4), int(im_h // 4 * 4)))
        #     for i in range(len(haze_image)):
        #         img = np.array(haze_image[i]).astype('float')
        #         img = torch.from_numpy(img.transpose((2, 0, 1))).float()
        #         edge = edge_compute(img)
        #         haze = torch.cat((img, edge), dim=0) - 128
        #         haze = haze.unsqueeze_(0)
        #         if i == 0:
        #             hazes = haze
        #         else:
        #             hazes = torch.cat((hazes, haze), dim = 0)
        #     pred = model(hazes, 0, True, False)
        #     preds = torch.split(pred, 1, dim = 0)
        #     out_imgs = list()
        #     for img in preds:
        #         dehaze = img.float().round().clamp(0, 255)
        #         out_img = dehaze[0].cpu().numpy().astype(np.uint8).transpose(1, 2, 0)
        #         out_imgs.append(out_img)
        #     return out_imgs


def run_dehazingmodel_image(model, image_path):
    print("dehazing image.")
    haze_image = Image.open(image_path).convert('RGB')
    ts = run_dehazingmodel(model, haze_image, 0)
    #vutils.save_image(ts, image_path.replace('input', 'output'))
    ts.save(image_path.replace('input', 'output'))
    print("finish dehazing.")

def run_dehazingmodel_video(model, video_path, tmp = False):
    print("dehazing video.")
    haze_images, fps = videoToImages(video_path)
    print("frames before:", len(haze_images))
    #print(type(haze_images[0]))
    images = list()
    batch = list()
    #print(len(haze_images))
    for i in range(len(haze_images)):
        if i % 2 != 0:
            #if i % 2 == 0:
            batch.append(Image.fromarray(haze_images[i]))
        else:
            if i != 0:
                t1 = datetime.datetime.now()
                ts = run_dehazingmodel(model, batch, 1)
                t2 = datetime.datetime.now()
                print((t2-t1).total_seconds())
                images.extend(ts)
            batch.clear()
            batch.append(Image.fromarray(haze_images[i]))
    if len(batch) != 0:
        ts = run_dehazingmodel(model, batch, 1)
        images.extend(ts)
    print("fps:", fps)
    if tmp:
        print("finish dehazing.")
        return haze_images, images, fps
    else:
        #print(type(images[0]))
        videoMerge(haze_images, images, fps, video_path.replace('input', 'output'))
        #imagesToVideo(images, fps, video_path.replace('input', 'output'))
        print("frames after:", len(images))
        #imagesToVideo(images, fps, video_path.replace('input', 'output'))
        print("finish dehazing.")



        ###################
