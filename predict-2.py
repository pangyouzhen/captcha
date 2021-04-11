# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 20:07:17 2019

@author: icetong
"""

import torch
import torch.nn as nn
from models import CNN
from datasets import img_loader
from torchvision.transforms import Compose, ToTensor
from train import num_class
from pathlib import Path

model_path = './checkpoints/model.pth'

source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97 + 26)]
alphabet = ''.join(source)


def predict(img_dir=Path('./captcha')):
    transforms = Compose([ToTensor()])
    for i in img_dir.glob("*png"):
        print(i.name)
        img = img_loader('./captcha/%s' % i.name)
        img = transforms(img)
        cnn = CNN()
        if torch.cuda.is_available():
            cnn = cnn.cuda()
        cnn.load_state_dict(torch.load(model_path))

        img = img.view(1, 3, 36, 120).cuda()
        output = cnn(img)

        output = output.view(-1, 36)
        output = nn.functional.softmax(output, dim=1)
        output = torch.argmax(output, dim=1)
        output = output.view(-1, num_class)[0]

        pred = ''.join([alphabet[i] for i in output.cpu().numpy()])
        print(pred)


if __name__ == "__main__":
    predict()
