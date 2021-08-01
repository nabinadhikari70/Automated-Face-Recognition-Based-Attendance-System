from retinaface import RetinaFace
from matplotlib import pyplot as plt
from flask import Flask, request, render_template, jsonify, Markup, session, redirect, url_for
import os
from werkzeug.utils import secure_filename
import cv2
import time

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'key'


def face_detection(image_loc):
    faces = RetinaFace.detect_faces(img_path=image_loc)
    image = cv2.imread(image_loc)
    for face in faces.items():
        data = face[1]["facial_area"]
        # formula = (y1:y2+1 ,x1:x2+1)
        crop = image[data[1]:data[3]+1, data[0]:data[2]+1]
        location = './static/img/faces/' + \
            str(face[0])+'.jpg'
        cv2.imwrite(location, crop)
    return faces


host_add = '127.0.0.1'
port_add = 5000


@app.route('/')
def index():
    return render_template('login.html')

# webpage where user can provide image


@app.route('/detectfaces', methods=['GET', 'POST'])
def detectfaces():
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files:
            message = "Please Select a Image first"
        elif file.filename == '':
            message = "Please Select a Image first"
        else:
            message = "Image accepted"
            filename = secure_filename("image_"+str(int(time.time()))+".jpg")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename_full = UPLOAD_FOLDER + filename
            info = face_detection(filename_full)
        context = {'message': message, 'image_info': info,
                   'img_time': str(int(time.time()))}
        print(context)
        return render_template('detectfaces.html', context=context, len=len(info) , zip=zip)
    else:
        return render_template('detectfaces.html', context={}, len=0 , zip = zip)


# Running the app
if __name__ == "__main__":
    app.run(host=host_add, port=port_add, debug=True)
    app.jinja_env.filters['zip'] = zip
