import cv2
import numpy as np
import dlib

# Load the pre-trained face recognition model from dlib
face_rec_model_path = "models/dlib_face_recognition_resnet_model_v1.dat"
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

# Load the pre-trained shape predictor model from dlib
shape_predictor_path = "models/shape_predictor_68_face_landmarks.dat"
shape_predictor = dlib.shape_predictor(shape_predictor_path)

# Load the Dlib HOG face detector
hog_face_detector = dlib.get_frontal_face_detector()

# returns a list of tuples containing the face image, face rectangle and face vector
def detect_faces(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use the Dlib HOG face detector
    detections = hog_face_detector(gray_frame, 1)
    
    faces_set = []
    for detection in detections:
        x, y, w, h = (detection.left(), detection.top(), detection.width(), detection.height())
        face = frame[y:y+h, x:x+w]
        face_vector = extract_features(frame, (x, y, w, h))
        faces_set.append((face, (x, y, w, h), face_vector))

    return faces_set

def extract_features(frame, face_rect):
    x, y, w, h = face_rect
    rect = dlib.rectangle(x, y, x+w, y+h)
    shape = shape_predictor(frame, rect)
    face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
    return np.array(face_descriptor)

