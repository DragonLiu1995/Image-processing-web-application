# Xiulong Liu
# EE568
# Create an Image processing(segmentation) backend to
# demonstrate cluster algorithms
from flask import Flask, render_template, jsonify, make_response, request, redirect, abort, Response
import cv2
import numpy as np
import os
#from werkzeug.utils import secure_filename
import flask_cors
from seg import segment_with_kmeans, segment_with_GMM, segment_with_Ostu
#from multiprocessing import Pool

app = Flask(__name__)  # Create an instance of Flask class
flask_cors.CORS(app)
UPLOAD_FOLDER = os.path.basename('upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# At the / route, render quotes.html from templates
@app.route('/')
@flask_cors.cross_origin()
def load_page():
    return render_template('app.html')

def responder(content, item):
    retval, buffer = cv2.imencode('.jpg', item)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = content  # default to 'image/jpg'
    return response


@app.route('/image', methods=['GET', 'POST'])
@flask_cors.cross_origin()
def read_image():
  img = cv2.imread('1.JPG')
  if request.method == 'POST':
      file = request.files['file']
      f = os.path.join(app.config['UPLOAD_FOLDER'], '1.JPG')
      file.save(f)
      img = cv2.imread('upload/1.JPG')
  return jsonify({"success": "Upload image successfully!"})

@app.route('/result', methods=['GET'])
@flask_cors.cross_origin()
def segImage():
     approach = request.args.get('approach', default = "kmeans", type = str)
     cluster = 0
     out_img = 0
     if not approach == 'Ostu':
         cluster = request.args.get('cluster', default = 3, type = int)
     if os.path.exists('upload/1.JPG'):
         filename = 'upload/1.JPG'
         img = cv2.imread(filename)
         if approach == 'kmeans':
             out_img = segment_with_kmeans(cluster, img)
         elif approach == 'GMM':
             out_img = segment_with_GMM(cluster, img)
         elif approach == 'Ostu':
              out_img = segment_with_Ostu(img)
         #pool = Pool(processes=1)
         #pool.apply_async(segement_with_kmeans, [3, filename])
     else:
         abort(404)
         abort(Response('The image is not uploaded yet!'))
     return responder('image/jpg', out_img)

# Run the app on localhost, port 8080 with debug mode on
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
