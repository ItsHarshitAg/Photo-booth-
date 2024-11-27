from flask import Flask, request, jsonify, render_template, send_file
from io import BytesIO
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        image_data = image_file.read()

        # Use rembg to remove the background
        output_image = remove(image_data)
        output_pil = Image.open(BytesIO(output_image))

        # Optional: Resize the image to reduce memory consumption (adjust as needed)
        output_pil = output_pil.resize((1024, 1024))

        # Save image to memory buffer
        output_buffer = BytesIO()
        output_pil.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return send_file(output_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get the port number from the environment or default to 5000
# port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
