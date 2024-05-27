import os
import time
import webbrowser
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from src.forms import MainForm
import cv2
import numpy as np
import matplotlib.pyplot as plt

SECRET_KEY = os.urandom(32)
IMAGES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/images'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

csrf = CSRFProtect(app)


@app.route("/")
def index():
    form = MainForm()
    modified = request.args.get('modified', False)
    base_file = request.args.get('base_file', "")
    modified_file = request.args.get('modified_file', "")
    return render_template("index.html", form=form, modified=modified,
                           base_file=base_file, modified_file=modified_file)


@app.route("/images/<filename>")
def image(filename):
    return send_from_directory("images", filename)


@app.route("/modify", methods=["POST"])
def modify():
    form = MainForm(request.form)
    effect = form.effect.data
    rotation = form.rotation.data
    translation = form.translation.data
    translation_pixels = form.translation_pixels.data
    scale = form.scale.data
    edge_highlighting = form.edge_highlighting.data
    mirroring = form.mirroring.data
    histogram = form.histogram.data
    image = request.files["file"]
    images_path = IMAGES_PATH
    timestamp = time.time()
    image.save(f'{images_path}/imagem-{timestamp}-base.jpg')
    image_to_modify = cv2.imread(f'{images_path}/imagem-{timestamp}-base.jpg')

    if effect != "no_effect":
        apply_color_effect(image_to_modify, timestamp, effect)
        image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')
    else:
        image_being_modified = image_to_modify

    if rotation == "90_degrees":
        rotate_90_degrees(image_being_modified, timestamp)
        image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')
    elif rotation == "180_degrees":
        rotate_180_degrees(image_being_modified, timestamp)
        image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')
    elif rotation == "270_degrees":
        rotate_270_degrees(image_being_modified, timestamp)
        image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')
    elif rotation == "no_rotation":
        pass

    translate(image_being_modified, timestamp, translation, translation_pixels)
    image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')

    change_scale(image_being_modified, timestamp, scale)
    image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')

    if edge_highlighting:
        highlight_edges(image_being_modified, timestamp)
        image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')

    if mirroring:
        mirror(image_being_modified, timestamp)
        image_being_modified = cv2.imread(f'{images_path}/imagem-{timestamp}-modified.jpg')

    if histogram:
        make_histogram(image_being_modified, timestamp)
        webbrowser.open_new_tab("{0}/images/imagem-{1}-histogram.jpg".format(url_for("index"), timestamp))

    base_file = f'imagem-{timestamp}-base.jpg'
    modified_file = f'imagem-{timestamp}-modified.jpg'

    return redirect(url_for("index", modified=True, base_file=base_file,
                            modified_file=modified_file))


def apply_color_effect(image, image_timestamp: float, effect: str) -> None:
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            (blue, green, red) = image[y, x]
            if effect == "black_white":
                image[y, x] = (red, red, red)
            elif effect == "red":
                image[y, x] = (0, 0, red)
            elif effect == "green":
                image[y, x] = (0, green, 0)
            elif effect == "blue":
                image[y, x] = (blue, 0, 0)
            elif effect == "inverted":
                image[y, x] = (red, green, blue)
    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', image)


def rotate_90_degrees(image, image_timestamp: float) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    # Cria uma nova imagem com as dimensões invertidas para a rotação de 90 graus
    rotated_image = np.zeros((width, height, 3), dtype=np.uint8)

    # Percorre a imagem original e rotaciona cada pixel manualmente
    for y in range(height):
        for x in range(width):
            rotated_image[x, height - y - 1] = image[y, x]

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', rotated_image)


def rotate_180_degrees(image, image_timestamp: float) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    # Cria uma nova imagem com as mesmas dimensões para a rotação de 180 graus
    rotated_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Percorre a imagem original e rotaciona cada pixel manualmente
    for y in range(height):
        for x in range(width):
            rotated_image[height - y - 1, width - x - 1] = image[y, x]

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', rotated_image)


def rotate_270_degrees(image, image_timestamp: float) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    # Cria uma nova imagem com as dimensões invertidas para a rotação de 270 graus
    rotated_image = np.zeros((width, height, 3), dtype=np.uint8)

    # Percorre a imagem original e rotaciona cada pixel manualmente
    for y in range(height):
        for x in range(width):
            rotated_image[width - x - 1, y] = image[y, x]

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', rotated_image)


def translate(image, image_timestamp: float, direction: str, pixels: int) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    # Cria uma nova imagem preenchida com zeros (preta)
    translated_image = np.zeros_like(image)

    if direction == "up":
        for y in range(pixels, height):
            for x in range(width):
                translated_image[y - pixels, x] = image[y, x]
    elif direction == "down":
        for y in range(height - pixels):
            for x in range(width):
                translated_image[y + pixels, x] = image[y, x]
    elif direction == "left":
        for y in range(height):
            for x in range(pixels, width):
                translated_image[y, x - pixels] = image[y, x]
    elif direction == "right":
        for y in range(height):
            for x in range(width - pixels):
                translated_image[y, x + pixels] = image[y, x]

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', translated_image)


def change_scale(image, image_timestamp: float, percentage: str) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    if percentage == "100_percent":
        scale_percent = 100
    elif percentage == "25_percent":
        scale_percent = 25
    elif percentage == "50_percent":
        scale_percent = 50
    elif percentage == "75_percent":
        scale_percent = 75
    elif percentage == "150_percent":
        scale_percent = 150
    elif percentage == "200_percent":
        scale_percent = 200

    # Calcula as novas dimensões da imagem
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)

    # Cria uma nova imagem com as novas dimensões
    resized_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Escala a imagem manualmente
    for y in range(new_height):
        for x in range(new_width):
            orig_x = int(x / (scale_percent / 100))
            orig_y = int(y / (scale_percent / 100))
            if orig_x < width and orig_y < height:
                resized_image[y, x] = image[orig_y, orig_x]

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', resized_image)


def highlight_edges(image, image_timestamp: float) -> None:
    # Define os kernels de Sobel para a detecção de bordas
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32)

    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]], dtype=np.float32)

    # Obtém as dimensões da imagem
    height, width = image.shape[:2]

    # Cria uma imagem para armazenar a magnitude dos gradientes
    edge_image = np.zeros_like(image, dtype=np.float32)

    # Aplica os kernels de Sobel manualmente
    for y in range(1, height-1):
        for x in range(1, width-1):
            gx = np.sum(sobel_x * image[y-1:y+2, x-1:x+2])
            gy = np.sum(sobel_y * image[y-1:y+2, x-1:x+2])
            edge_image[y, x] = np.sqrt(gx**2 + gy**2)

    # Normaliza a imagem resultante para o intervalo [0, 255]
    edge_image = np.clip(edge_image / np.max(edge_image) * 255, 0, 255).astype(np.uint8)

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', edge_image)


def mirror(image, image_timestamp) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    # Cria uma nova imagem com as mesmas dimensões
    mirrored_image = np.zeros_like(image)

    # Espelha a imagem horizontalmente
    for y in range(height):
        for x in range(width):
            mirrored_image[y, width - x - 1] = image[y, x]

    cv2.imwrite(f'{IMAGES_PATH}/imagem-{image_timestamp}-modified.jpg', mirrored_image )


def make_histogram(image, image_timestamp) -> None:
    # Obtém a altura e largura da imagem
    height, width = image.shape[:2]

    # Calcula o histograma para cada canal de cor manualmente
    hist_channels = np.zeros((256, 3), dtype=np.uint32)

    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            hist_channels[pixel[0], 0] += 1  # Canal azul
            hist_channels[pixel[1], 1] += 1  # Canal verde
            hist_channels[pixel[2], 2] += 1  # Canal vermelho

    # Plota os histogramas para cada canal de cor
    plt.figure()
    plt.title("Histogramas da Imagem Colorida")
    plt.xlabel("Intensidade de Pixel")
    plt.ylabel("Número de Pixels")
    colors = ('b', 'g', 'r')
    for i, color in enumerate(colors):
        plt.plot(hist_channels[:, i], color=color, label=f'Canal {color.upper()}')
    plt.legend()
    plt.xlim([0, 256])

    plt.savefig(f'{IMAGES_PATH}/imagem-{image_timestamp}-histogram.jpg')


if __name__ == "__main__":
    app.run(debug=True)
