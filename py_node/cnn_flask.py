import json

from flask import Flask, request
from cnn import cnn_pred, crop_captcha
from pathlib import Path

app = Flask(__name__)
path = Path("/tmp/untitled/")


@app.route("/cnn", methods=["GET"])
def reader():
    crop_captcha(path)
    pred = cnn_pred(path)
    return pred


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8081, debug=True)
