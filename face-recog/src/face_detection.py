import numpy as np
from PIL import Image
import logging
import insightface
from insightface.app import FaceAnalysis


# 'providers' tells the app to use CUDA (GPU) first
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640)) # ctx_id=0 targets the first GPU



# returns a list of tuples containing the face image, face rectangle and face vector
def detect_faces(frame):
    frame_np = np.array(frame)
    gray_frame = frame.convert('L')
    
    # Use the face detector
    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    detections = face_detector(np.array(gray_frame), 1)
    
    logging.debug(f"Number of faces detected: {len(detections)}")

    faces_set = []
    for detection in detections:
        detection = getattr(detection, "rect", detection)  # For CNN detector/HOG compatibility
        x, y, w, h = (detection.left(), detection.top(), detection.width(), detection.height())
        face = frame_np[y:y+h, x:x+w]
        face_vector = extract_features(frame_np, (x, y, w, h))
        # This below is to fix a bug that I don't understand (yet ?) - sometimes face is None ?
        if face is None:
            print("face is None - strange !")
            continue
        face_rgb = Image.fromarray(face)
        faces_set.append((face_rgb, (x, y, w, h), face_vector))

    return faces_set

def extract_features(frame, face_rect):
    x, y, w, h = face_rect
    rect = dlib.rectangle(x, y, x+w, y+h)
    shape = shape_predictor(frame, rect)
    face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
    return np.array(face_descriptor)

