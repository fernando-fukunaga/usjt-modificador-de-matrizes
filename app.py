import os
import time
import webbrowser
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from src.forms import MainForm
import cv2

SECRET_KEY = os.urandom(32)
IMAGES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/images'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

csrf = CSRFProtect(app)


@app.route("/")
def index():
    form = MainForm()
    return render_template("index.html", form=form)


@app.route("/images/<filename>")
def image(filename):
    return send_from_directory("images", filename)


@app.route("/modify", methods=["POST"])
def modify():
    form = MainForm(request.form)
    effect = form.effect.data
    image = request.files["file"]
    images_path = IMAGES_PATH
    timestamp = time.time()
    image.save(f'{images_path}/imagem-{timestamp}-base.jpg')
    image_to_modify = cv2.imread(f'{images_path}/imagem-{timestamp}-base.jpg')

    if effect == "blackwhite":
        modify_to_black_and_white(image_to_modify, timestamp)
    elif effect == "red":
        modify_to_red(image_to_modify, timestamp)
    elif effect == "green":
        modify_to_green(image_to_modify, timestamp)
    elif effect == "blue":
        modify_to_blue(image_to_modify, timestamp)
    elif effect == "inverted":
        modify_to_inverted(image_to_modify, timestamp)

    webbrowser.open_new_tab(f'http://localhost:5000/images/imagem-{timestamp}-modified.jpg')
    return redirect(url_for("index"))


def modify_to_black_and_white(image, image_timestamp: float) -> None:
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (blue, green, red) = image[y, x]
            image[y, x] = (red, red, red)
    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', image)


def modify_to_red(image, image_timestamp: float) -> None:
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (blue, green, red) = image[y, x]
            image[y, x] = (0, 0, red)
    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', image)


def modify_to_blue(image, image_timestamp: float) -> None:
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (blue, green, red) = image[y, x]
            image[y, x] = (blue, 0, 0)
    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', image)


def modify_to_green(image, image_timestamp: float) -> None:
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (blue, green, red) = image[y, x]
            image[y, x] = (0, green, 0)
    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', image)


def modify_to_inverted(image, image_timestamp: float) -> None:
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (blue, green, red) = image[y, x]
            image[y, x] = (red, green, blue)
    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', image)


if __name__ == "__main__":
    app.run(debug=True)
