# cmake, dlib, facereco, cv2, numpy


# for now data base= dictionary { scholarId: encoding(array of 128) }
# later it will be stored in a csv file


import cv2
import os
import numpy as np
import face_recognition
from csv import writer, reader

# name: encoding
peopleDict = {}


def getImg2Enc(image):
    """
    :param image: image read by cv2
    :return: array : encoding
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]  # since only one face will be there in input "image"
    return encode


def findIdentity(tarImgEnc, dictP):
    """
    :param tarImgEnc: targeted image encoding : array of 128 * 1
    :param dictP: dict of encodings : {name:encd}
    :return: most similar scholar id or -1
    """
    encodings = list(dictP.values())
    schIds = list(dictP.keys())
    matches = face_recognition.compare_faces(encodings, tarImgEnc)
    faceDis = face_recognition.face_distance(encodings, tarImgEnc)
    matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
        return schIds[matchIndex]
    return '-1'


def getPresStds(img):
    """
    :param img: image read by cv2 or np array
    :return: list of present students
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodes = face_recognition.face_encodings(img)
    presStds = []

    if not os.path.exists('registeredStds.csv'):
        return ['-1']

    # make that name: enc dict from csv
    regDict = {}
    with open('registeredStds.csv', 'r') as fObj:
        content = reader(fObj)
        for row in content:
            regDict[row[0]] = [float(value) for value in row[1:]]

    for enc in encodes:
        res = findIdentity(enc, regDict)
        if res == '-1':
            continue
        else:
            presStds.append(res)

    return presStds


def checkPresence(imgPath):
    """
    :param imgPath: str: image path
    :return: None
    """
    img = cv2.imread(imgPath)
    imgEnc = getImg2Enc(img)
    res = findIdentity(imgEnc, peopleDict)

    if res == -1:
        print("Not found in DB")
    else:
        print(res + " is present.")


def regImg(name, img):
    """
    :param name: str : name
    :param img: string: image read by cv2 or np array
    :return: true if registered else false
    """
    # get the encodings
    imgEnc = getImg2Enc(img)

    # check if the file (registerdStds.csv) exist if not make one
    regFilePath = 'registeredStds.csv'
    if not os.path.exists(regFilePath):
        open(regFilePath, 'a').close()

    # append the info to the file
    to_save = [name] + imgEnc.tolist()
    with open(regFilePath, 'a', newline='') as fObj:
        writer_obj = writer(fObj)
        writer_obj.writerow(to_save)
        fObj.close()

    return True


def imageShow(path):
    """
    :param path: str: image path
    :return: None
    """
    print(path)
    img = cv2.imread(path)
    if img is not None:
        window_name = 'image'
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Image cant be read !!! ")

