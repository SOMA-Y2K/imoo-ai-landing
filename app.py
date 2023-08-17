from flask import Flask, jsonify, request
from flask_restx import Resource , Api
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True

CORS(app)

UPLOAD_FOLDER = "path_to_your_upload_folder"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def connect():
    return "hi"


@app.route('/image', methods=['POST'])
def upload_image():
    try:
        print(request.files)
        if 'image' in request.files:
            image = request.files['image']
            if image.filename == '':
                return jsonify({"error": "No selected file"})
            if image and allowed_file(image.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filename)
                return jsonify({"message": "Image uploaded and saved successfully"})
            else:
                return jsonify({"error": "Invalid file format"})
        else:
            return jsonify({"error": "No image provided"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__' :
    app.run(debug =True)

