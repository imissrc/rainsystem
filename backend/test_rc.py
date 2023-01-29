from django.test import TestCase

import backend.deal_derain as deal_derain
from pathlib import Path
import os
from backend.derain.load_model import createMoss
from backend.derain.load_model import createMprnet

class DerainTestCase(TestCase):
    def testDerainVideoMOSS(self):
        derain_model = createMoss()
        cur_path = Path(__file__).resolve().parent
        input_video_path = os.path.join(cur_path, "../resources/deraining/output-moss-10-1.avi")
        output_video_path = os.path.join(cur_path, "../resources/deraining/output-moss-10-2.avi")
        deal_derain.getVideoDerain(derain_model, input_video_path, output_video_path)

    def testDerainImageMOSS(self):
        derain_model = createMoss()
        cur_path = Path(__file__).resolve().parent
        input_image_path = os.path.join(cur_path, "../resources/deraining/input-7850.png")
        output_image_path = os.path.join(cur_path, "../resources/deraining/output-moss-7850.png")
        deal_derain.getImageDerain(derain_model, input_image_path, output_image_path)

    def testDerainVideoMPRNet(self):
        derain_mprnet_model = createMprnet()
        cur_path = Path(__file__).resolve().parent
        input_video_path = os.path.join(cur_path, "../resources/deraining/10.avi")
        output_video_path = os.path.join(cur_path, "../resources/deraining/output-mprnet-10.avi")
        deal_derain.getVideoDerain(derain_mprnet_model, input_video_path, output_video_path, 'mprnet')

    def testDerainImageMPRNet(self):
        derain_mprnet_model = createMprnet()
        cur_path = Path(__file__).resolve().parent
        input_image_path = os.path.join(cur_path, "../resources/deraining/4099.png")
        output_image_path = os.path.join(cur_path, "../resources/deraining/output-mprnet-4099.png")
        deal_derain.getImageDerain(derain_mprnet_model, input_image_path, output_image_path, 'mprnet')