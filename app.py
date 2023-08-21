from flask import Flask, jsonify, request, send_file
from flask_restx import Resource , Api
from PIL import Image
import zipfile
from flask_cors import CORS
import requests
import os
import io

from main import run_main_script

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

                input_filename = "./VITON-HD/test_pairs_unpaired_1018.txt"
                output_lines = [f"00888_00.png {image.filename} upper",
                                f"00920_00.png {image.filename} upper",
                                f"01767_00.png {image.filename} upper",
                                f"01839_00.png {image.filename} upper",
                                f"02636_00.png {image.filename} upper",
                                f"03178_00.png {image.filename} upper",
                                f"03884_00.png {image.filename} upper",
                                f"04071_00.png {image.filename} upper"]
                                
                with open(input_filename, "w") as output_file:
                    for line in output_lines :
                        output_file.write(f"{line}\n")
        
                folder_name = os.path.splitext(image.filename)[0]
                run_main_script(folder_name)


      
                output_images = []
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
                    sample_directory = f"sample/{folder_name}"
                    for root, dirs, files in os.walk(sample_directory):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Add each file to the zip archive
                            zip_archive.write(file_path, os.path.relpath(file_path, sample_directory))


                    # for i, output_img in enumerate(output_images):
                        
                    #     #print(f"Image {i}: Size = {output_img.size}, Mode = {output_img.mode}")
                    #     output_filename = f'output_{i}.png'
                        
                    #     output_img.save(output_filename, format='png')
                    #     print(output_img)
                    #     output_filenames.append(output_filename)
                    #     zip_archive.write(output_filename)
        
               
                zip_buffer.seek(0)
                for output_filename in output_filenames:
                    os.remove(output_filename)
                print(zip_buffer)
                return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='output_images.zip')
       
            else:
                return jsonify({"error": "Invalid file format"})
        else:
            return jsonify({"error": "No image provided"})
    except Exception as e:
         return jsonify({"error": str(e)})

if __name__ == '__main__' :
    app.run(debug =True, host='0.0.0.0')

