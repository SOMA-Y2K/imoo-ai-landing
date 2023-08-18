from flask import Flask, jsonify, request, send_file
from flask_restx import Resource , Api
from PIL import Image
import zipfile
from flask_cors import CORS
import requests
import os
import io

app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = "./images/"

CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def connect():
    return "hi"


@app.route('/image', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello World"})


@app.route('/image', methods=['POST'])
def upload_image():
    try:
    
     
        if 'image' in request.files:
            image = request.files['image']

            
            if image.filename == '':
                return jsonify({"error": "No selected file"})
            if image and allowed_file(image.filename):
                image_data = image.read()
                filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                # module for virtual fitting clothes
                # 4 output images will be made 
                #image.save(filename)
                pil_image = Image.open(io.BytesIO(image_data))
                
      
                output_images = [pil_image.copy() for _ in range(4)]
                output_filenames = []
              
                
                # zip_buffer = io.BytesIO()
                # with zipfile.ZipFile(zip_buffer, 'w') as zip_archive :
                #     for i, output_img in enumerate(output_images) :
                     
                #         output_filename = f'output_{i}.png'
                #         output_img.save(output_filename)
                #         output_filenames.append(output_filename)                
                #         zip_archive.write(output_filename)
                        
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_archive:
                    for i, output_img in enumerate(output_images):
                        
                        #print(f"Image {i}: Size = {output_img.size}, Mode = {output_img.mode}")
                        output_filename = f'output_{i}.png'
                        
                        output_img.save(output_filename, format='png')
                        print(output_img)
                        output_filenames.append(output_filename)
                        zip_archive.write(output_filename)
        
               
                zip_buffer.seek(0)
                #for output_filename in output_filenames:
                #    os.remove(output_filename)
                print(zip_buffer)
                return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='output_images.zip')
       
            else:
                return jsonify({"error": "Invalid file format"})
        else:
            return jsonify({"error": "No image provided"})
    except Exception as e:
         return jsonify({"error": str(e)})

if __name__ == '__main__' :
    app.run(debug =True)

