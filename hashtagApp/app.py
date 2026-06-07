from flask import Flask, request, render_template
from PIL import Image
import base64
import io

import config
from utils import get_text_info

app = Flask(__name__)


def encode_image(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def process_image(image: Image.Image):
    message = get_text_info(image)
    bw_image = image.convert("1")
    gs_image = image.convert("L")
    size = (config.IMAGE_SIZE, config.IMAGE_SIZE)
    return (
        encode_image(image.resize(size)),
        encode_image(bw_image.resize(size)),
        encode_image(gs_image.resize(size)),
        message,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    image = bw_image = gs_image = text = None
    if request.method == "POST":
        if "image" not in request.files:
            error = "No image uploaded."
        else:
            file = request.files["image"]
            if file.filename == "":
                error = "No image selected."
            else:
                image, bw_image, gs_image, text = process_image(Image.open(file))
    return render_template(
        "index.html",
        error=error,
        image=image,
        bw_image=bw_image,
        gs_image=gs_image,
        text=text,
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
