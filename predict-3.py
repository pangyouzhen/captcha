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
import execjs
import requests

with open(r'/home/pang/Downloads/aes.min.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('/data/project/learn_code/other/encrty.js', 'r', encoding='utf-8') as fs:
    js_file = fs.read()

ct = execjs.compile(js, cwd=r'/usr/lib/node_modules')
js_load = execjs.compile(js_file, cwd=r'/usr/lib/node_modules')
uname = js_load.call('thsencrypt.encode', '')
passwd = js_load.call('thsencrypt.encode', '')
v = ct.call("v")
print(uname)
print(ct.call("v"))
model_path = './checkpoints/model.pth'

headers1 = {
    'Host': 'upass.iwencai.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'http://upass.iwencai.com/login?act=loginByIframe&view=public&source=iwc_web&main=7&detail=3&redir=http%3A%2F%2Fwww.iwencai.com%2Funifiedwap%2Flogin-sso.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'PHPSESSID=knstqaqbslsmns9ql3cdbqd91a91ee0n; cid=0bdf07ddd90f80d8706fd264827abd8a1618119272; v=%s' % v
}

source = [str(i) for i in range(0, 10)]
source += [chr(i) for i in range(97, 97 + 26)]
alphabet = ''.join(source)
screenImg = "%s.png" % "ths_captcha"
a = requests.get("http://upass.iwencai.com/captcha/buildcaptcha?type=flat&16768&0.4653998146883518", headers=headers1)
with open(screenImg, "wb") as f:
    f.write(a.content)


def predict():
    transforms = Compose([ToTensor()])
    img = img_loader('ths_captcha.png')
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
    return pred


pred = predict()
print(pred)

url = "http://upass.iwencai.com/login/dologinreturnjson2"

payload = {
    "uname": "%s" % uname,
    "passwd": "%s" % passwd,
    "captcha": "%s" % pred,
    "longLogin": "on",
    "rsa_version": "default_4",
    "source": "iwc_web"
}
headers = {
    'POST': '/login/dologinreturnjson2 HTTP/1.1',
    'Host': 'upass.iwencai.com',
    'Connection': 'keep-alive',
    "hexin-v": "%s" % v,
    'Content-Length': '450',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://upass.iwencai.com',
    'Referer': 'http://upass.iwencai.com/login?act=loginByIframe&view=public&source=iwc_web&main=7&detail=3&redir=http%3A%2F%2Fwww.iwencai.com%2Funifiedwap%2Flogin-sso.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'PHPSESSID=knstqaqbslsmns9ql3cdbqd91a91ee0n; cid=0bdf07ddd90f80d8706fd264827abd8a1618119272; v=%s' % v
}

response = requests.request("POST", url, headers=headers, data=payload)
response.encoding = 'utf-8'
print(response.text)
cookies = response.cookies
cookie = requests.utils.dict_from_cookiejar(cookies)
print(cookie)
