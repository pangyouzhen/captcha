import muggle_ocr
from pathlib import Path

path = Path("./")
print(path.absolute())
captcha_path = path / "captcha"
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)


def get_png(items):
    for i in items:
        with open("%s" % i, "rb") as f:
            captcha_bytes = f.read()
        text = sdk.predict(image_bytes=captcha_bytes)
        if len(text) == 6:
            print(i.stem, text)
        yield text

def get_png2():
    for i in captcha_path.glob("*png"):
        with open("%s" % i.name, "rb") as f:
            captcha_bytes = f.read()
        text = sdk.predict(image_bytes=captcha_bytes)
        if len(text) == 6:
            print(i.stem, text)
        yield text

if __name__ == '__main__':
    items = [i for i in captcha_path.glob("*png")]
    a = 0
    for j in get_png(items):
        a += 1
        if a > 200:
            break
