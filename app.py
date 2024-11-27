# # import os
# # from io import BytesIO
# # import cv2
# # import numpy as np
# # from flask import Flask, request, jsonify, send_file
# # from PIL import Image
# # import logging

# # app = Flask(__name__)

# # # Set up logging for better debugging
# # logging.basicConfig(level=logging.INFO)

# # @app.route('/')
# # def home():
# #     return "Welcome to the Background Removal API!"

# # def remove_background_opencv(image_data):
# #     # Convert image data to a numpy array
# #     nparr = np.frombuffer(image_data, np.uint8)
# #     img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

# #     # Check if the image is loaded successfully
# #     if img is None:
# #         raise ValueError("Could not read the image.")

# #     # Convert to RGB (OpenCV uses BGR by default)
# #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# #     # GrabCut algorithm for background removal
# #     mask = np.zeros(img_rgb.shape[:2], np.uint8)
# #     bgd_model = np.zeros((1, 65), np.float64)
# #     fgd_model = np.zeros((1, 65), np.float64)

# #     # Rectangular area where foreground is located (this is an approximate guess)
# #     rect = (10, 10, img_rgb.shape[1] - 10, img_rgb.shape[0] - 10)

# #     # Apply GrabCut algorithm
# #     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# #     # Modify mask to get the foreground
# #     mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# #     # Create the result image by applying the mask
# #     result = img_rgb * mask2[:, :, np.newaxis]

# #     # Convert result back to PIL Image
# #     return Image.fromarray(result, 'RGB')

# # @app.route('/remove-background', methods=['POST'])
# # def remove_background():
# #     try:
# #         # Check if an image file was uploaded
# #         if 'image' not in request.files:
# #             return jsonify({"error": "No image file provided"}), 400
        
# #         image_file = request.files['image']
        
# #         # Validate the file type
# #         if not image_file.content_type.startswith('image/'):
# #             return jsonify({"error": "Invalid file type. Please upload an image."}), 400
        
# #         # Read the image file
# #         image_data = image_file.read()

# #         # Remove the background using OpenCV
# #         output_pil = remove_background_opencv(image_data)

# #         # Save the result to a BytesIO buffer in PNG format
# #         output_buffer = BytesIO()
# #         output_pil.save(output_buffer, format="PNG")
# #         output_buffer.seek(0)

# #         # Return the processed image
# #         return send_file(output_buffer, mimetype='image/png')

# #     except Exception as e:
# #         logging.error(f"Error processing image: {str(e)}")
# #         return jsonify({"error": "An error occurred while processing the image."}), 500

# # if __name__ == '__main__':
# #     app.run(debug=True)


# from flask import Flask, request, jsonify, render_template, send_file
# from io import BytesIO
# from PIL import Image
# from rembg import remove

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/remove-background', methods=['POST'])
# def remove_background():
#     try:
#         if 'image' not in request.files:
#             return jsonify({"error": "No image file provided"}), 400

#         image_file = request.files['image']
#         image_data = image_file.read()

#         output_image = remove(image_data)
#         output_pil = Image.open(BytesIO(output_image))

#         output_buffer = BytesIO()
#         output_pil.save(output_buffer, format="PNG")
#         output_buffer.seek(0)

#         return send_file(output_buffer, mimetype='image/png')

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


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

if __name__ == '__main__':
    app.run(debug=True)