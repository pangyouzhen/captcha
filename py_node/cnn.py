from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from loguru import logger
from torchvision.transforms import Compose, ToTensor

from datasets import img_loader
from models import CNN
from train import num_class

model_path = '../checkpoints/model.pth'
# path = Path("./node_captcha")
source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97 + 26)]
alphabet = ''.join(source)

transforms = Compose([ToTensor()])
cnn = CNN()
if torch.cuda.is_available():
    cnn = cnn.cuda()
cnn.load_state_dict(torch.load(model_path))
transforms = Compose([ToTensor()])
cnn = CNN()
if torch.cuda.is_available():
    cnn = cnn.cuda()
cnn.load_state_dict(torch.load(model_path))
# q = path / "captcha_crop.png"


def crop_captcha(path):
    img = Image.open(path / "captcha.png")
    # print(img.size)  # (1920, 1080)
    cropped = img.crop((455, 294, 575, 330))  # (left, upper, right, lower)
    cropped.save("./captcha_crop.png")
    # print(Image.open("captcha_test/captcha_crop.png").size)


# res = True
def cnn_pred(q):
    img = img_loader(q)
    img = transforms(img)
    img = img.view(1, 3, 36, 120).cuda()
    output = cnn(img)
    output = output.view(-1, 36)
    output = nn.functional.softmax(output, dim=1)
    output = torch.argmax(output, dim=1)
    output = output.view(-1, num_class)[0]
    pred = ''.join([alphabet[i] for i in output.cpu().numpy()])
    logger.info(pred)
    return pred

# logger.info("模型加载完成")
# while res:
#     if q.exists():
#         print("find this file")
