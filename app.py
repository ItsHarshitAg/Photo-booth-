from flask import Flask, request, jsonify, render_template, send_file
from io import BytesIO
from PIL import Image
from rembg import remove

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

        output_image = remove(image_data)
        output_pil = Image.open(BytesIO(output_image))

        output_buffer = BytesIO()
        output_pil.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return send_file(output_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

port = int(os.environ.get('PORT', 10000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
