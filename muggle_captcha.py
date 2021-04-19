import muggle_ocr
import time
from pathlib import Path

sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

path = Path('.')


# 区分测试集和验证集
def main():
    t = [True] * 8
    t.append(False)
    t.append(False)
    a = 0
    print(path.absolute())
    for j in path.glob("*.png"):
        with open(j, "rb") as f:
            captcha_bytes = f.read()
        st = time.time()
        # 3. 调用预测函数
        text = sdk.predict(image_bytes=captcha_bytes)
        if len(str(text)) == 6:
            if t[a]:
                j.rename("../data/train/%s.png" % (text))
            else:
                j.rename("../data/test/%s.png" % text)
        a += 1
        if a > 9:
            a = 0


if __name__ == '__main__':
    main()
