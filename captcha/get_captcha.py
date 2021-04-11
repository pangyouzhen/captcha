import requests
import time
for i in range(10693, 50000):
    screenImg = "%s.png" % i
    a = requests.get("http://upass.iwencai.com/captcha/buildcaptcha?type=flat&98065&0.8018520822388477")
    with open(screenImg, "wb") as f:
        f.write(a.content)
