#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import flask
import os
import requests
import uuid

import tciconvert

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

BASE_PATH = "static/pictures"
PRIVATE_KEY = "PRIVATE-0409e958-cbac-4907-9cda-542370d9a624"


def error(text, code=400):
    return flask.jsonify({"error": text}), code


@app.route("/convert/", methods=["POST"])
def convert():
    hsid = flask.request.form.get("hashcashid", None)
    if hsid is None:
        return error("captcha missing")

    hs = requests.get(
        f"https://hashcash.io/api/checkwork/{hsid}?apikey={PRIVATE_KEY}"
    )

    try:
        hsdata = hs.json()
    except json.JSONDecodeError:
        return error("captcha not found")

    if hsdata["verified"]:
        return error("captcha reused")

    if hsdata["totalDone"] < 0.01:
        return error("captcha too weak")

    try:
        quality = int(flask.request.form.get("quality") or "6")
    except ValueError:
        return error("quality invalid")

    if not(1 <= quality <= 100):
        return error("quality not in range")

    image = flask.request.files.get("image", None)

    if image is None:
        return error("image missing")

    result_name = str(uuid.uuid4())

    try:
        tciconvert.encode(image, f"{BASE_PATH}/{result_name}.tci", quality)
    except Exception as e:
        return error(f"failed: {e}")

    tciconvert.decode(f"{BASE_PATH}/{result_name}.tci", f"{BASE_PATH}/{result_name}.png")

    return flask.redirect(f"/show/{result_name}/")


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/show/<uuid:image>/")
def show(image):
    return flask.render_template("show.html", image=image)


@app.route("/buy/")
def buy():
    return flask.redirect("https://www.tinkoff.ru/collectmoney/crowd/roskov.vladislav1/qe9gx6267/?moneyAmount=1337")


@app.route("/feed_SWJS0fbB23Vi/")
def feed():
    files = sorted([
        f"{BASE_PATH}/{filename}"
        for filename in os.listdir(BASE_PATH)
        if filename.endswith(".png")
    ], key=os.path.getmtime, reverse=True)

    count = len(files)
    offset = int(flask.request.args.get("offset", "0"))

    files = files[offset:offset+20]

    return flask.render_template("feed.html", files=files, offset=offset, count=count)

if __name__ == '__main__':
    app.run()
