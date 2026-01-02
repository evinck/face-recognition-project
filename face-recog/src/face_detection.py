import numpy as np
from PIL import Image
import logging
import insightface
from insightface.app import FaceAnalysis


# 'providers' tells the app to use CUDA (GPU) first
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
#app.prepare(ctx_id=0, det_thresh=0.9,det_size=(640, 640)) # ctx_id=0 targets the first GPU
app.prepare(ctx_id=0, det_size=(640, 640)) # ctx_id=0 targets the first GPU


# returns a list of tuples containing the face image, face rectangle and face vector
def detect_faces(frame):
    frame_np = np.array(frame)
    # find the faces in the frame
    faces = app.get(frame_np)
    logging.debug(f"Number of faces detected: {len(faces)}")

    # build the faces_set to return
    faces_set = []
    for face in faces:
        x, y, x2, y2 = face.bbox.astype(int)
        logging.debug(f"face.bbox: {x}, {y}, {x2}, {y2}")
        face_vector = face.normed_embedding
        # logging.debug(f"face.embedding : {face.embedding}")
        # logging.debug(f"face.normed_embedding : {face.normed_embedding}")
        face_rgb = Image.fromarray(frame_np[y:y2, x:x2])
        logging.debug(f"face_rgb size: {face_rgb.size}")
        faces_set.append((face_rgb, (x, y, x2, y2), face_vector))

    return faces_set
