import cv2
import numpy as np
import dlib

# Load the pre-trained face recognition model from dlib
face_rec_model_path = "models/dlib_face_recognition_resnet_model_v1.dat"
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

# Load the pre-trained shape predictor model from dlib
shape_predictor_path = "models/shape_predictor_68_face_landmarks.dat"
shape_predictor = dlib.shape_predictor(shape_predictor_path)

# returns a list of tuples containing the face image, face rectangle and face vector
def detect_faces(frame):
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    faces_set = []
    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face_vector = extract_features(frame, (x, y, w, h))
        faces_set.append((face,(x,y,w,h), face_vector))

    return faces_set

def extract_features(frame, face_rect):
    x, y, w, h = face_rect
    rect = dlib.rectangle(x, y, x+w, y+h)
    shape = shape_predictor(frame, rect)
    face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
    return np.array(face_descriptor)

