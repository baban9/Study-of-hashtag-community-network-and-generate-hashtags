from flask import Flask, request, render_template
from PIL import Image
import base64
import io
from utils import get_text_info

app = Flask(__name__)

def process_image(image):
    message =  get_text_info(image)
    bw_image = image.convert('1')
    # Convert image to grayscale
    gs_image = image.convert('L')
    # Resize images
    image = image.resize((400, 400))
    bw_image = bw_image.resize((400, 400))
    gs_image = gs_image.resize((400, 400))
    # Encode images as base64 strings
    buffered = io.BytesIO()
    image.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    buffered = io.BytesIO()
    bw_image.save(buffered, format='PNG')
    bw_img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    buffered = io.BytesIO()
    gs_image.save(buffered, format='PNG')
    gs_img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return img_str, bw_img_str, gs_img_str, message

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    image = None
    bw_image = None
    gs_image = None
    text = None
    if request.method == 'POST':
        if 'image' not in request.files:
            error = 'No image uploaded.'
        else:
            file = request.files['image']
            image = Image.open(file)
            if file.filename == '':
                error = 'No image selected.'
            else:
                image, bw_image, gs_image, text = process_image(image)
    return render_template('index.html', error=error, image=image, bw_image=bw_image, gs_image=gs_image, text=text)

if __name__ == '__main__':
    app.run(debug=True)
