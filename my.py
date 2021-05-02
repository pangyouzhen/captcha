from PIL import Image

img = Image.open("captcha.png")
# print(img.size)  # (1920, 1080)
cropped = img.crop((455, 294, 575, 330))  # (left, upper, right, lower)
cropped.save("./captcha_crop.png")
print(Image.open("captcha_test/captcha_crop.png").size)
# 上面是正向，即从左上角开始截图，下面的是从右下角开始反向截图
# from PIL import Image
#
# img = Image.open("./data/cut/thor.jpg")
# _width, _height = img.size
# cropped = img.crop((0, _height - 128, 512, _height))  # (left, upper, right, lower)
# cropped.save("./data/cut/leftlower_pil_cut.jpg")
img2 = (Image.open("./captcha/3.png"))
print(img2.size)
