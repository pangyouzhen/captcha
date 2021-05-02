import subprocess
import sys
from pathlib import Path

import pyautogui
from loguru import logger

from cnn import cnn_pred, crop_captcha
import time


def run_node():
    node = "node iwencai.js >> ./node_captcha/node_captcha.log"
    logger.info("node start")
    # todo
    child2 = subprocess.run(node.split(), shell=True, stdout=subprocess.PIPE)
    logger.info("node finish")


path = Path("./node_captcha")
res = True
run_node()
retry_time = 0
all_time = 0
while res:
    node_captcha = path / "node_captcha.log"
    if node_captcha.exists():
        logger.info("node log文件存在")
        with open(path / "node_captcha.log") as f:
            node_log = f.readlines()
        last_line = node_log[-1]
        if "用户输入验证码" == last_line:
            logger.info("输入验证码")
            crop_captcha(path)
            pred = cnn_pred(path / "captcha_crop.png")
            logger.info("验证码是 %s" % pred)
            for i in pred:
                pyautogui.press(i)
                logger.info("输入%s" % i)
            pyautogui.press('enter')
        elif "成功" in last_line:
            logger.info("成功")
            break
        elif "失败" in last_line:
            logger.info("失败")
            run_node()
            retry_time += 1
            logger.info("重试次数为%s" % retry_time)
            if retry_time > 3:
                break
    else:
        time.sleep(1)
        all_time += 1
        if all_time > 10000:
            break
        logger.info("文件不存在")
