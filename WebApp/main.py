from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import cv2
import os
import face_rec_web

app = Flask(__name__)


# print(os.listdir(os.getcwd()))

# this is working
# @app.route('/', methods=["GET", "POST"])
# def hello_world():
#     if request.method == "GET":
#         return render_template("uploader.html")
#     else:
#         return render_template("uploader.html", name="Hello post !")


# some information =================================================
# rdFile = request.files['file']
# rdFile = Image.open(rdFile) ====> this rdFile is image rad by PIL
#
# rdFilePIL = Image.open("DP_1.jpg") ====> image directly read by PIL from dir
#
# converted = np.array(rdFile) ===> image is converted into np array


@app.route('/', methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def registerStudents():
    if request.method == 'POST':
        img = Image.open(request.files['file'])
        img = np.array(img)
        name = request.form['nm']
        face_rec_web.regImg(name, img)
        return render_template("uploader.html", name="Registered successfully !")
    else:
        return render_template("uploader.html")


@app.route('/attendance', methods=["POST", "GET"])
def getAttendance():
    if request.method == 'POST':
        img = Image.open(request.files['file'])
        img = np.array(img)
        presStds = face_rec_web.getPresStds(img)
        if len(presStds) == 0:
            return "No students are present"
        if presStds[0] == '-1':
            return "No registered students found"

        return jsonify(presStds)
    else:
        return render_template("attendance.html")


if __name__ == '__main__':
    app.run(debug=True)

