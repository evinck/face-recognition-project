import cv2
from face_detection import detect_faces
from utils import load_config
from editor import Editor
from database import Database

# Load configuration
config = load_config()

def main():
    # Initialize the database
    database = Database(config["database_config"]["username"], config["database_config"]["password"])
    database.connect()

    # Initialize the editor 
    editor = Editor(database)
    editor.start_text_editor_thread()

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Detect faces in the frame
        faces = detect_faces(frame)
        #print(f"Detected faces: {len(faces)}") 

        # Insert face into database if needed
        for face in faces:
            # Draw rectangles around detected faces
            x, y, w, h = face[1]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            face_name=database.face_is_in_database2(face)
            if face_name == "":
                 print("New face detected - inserting into database") 
                 database.insert_face_in_database(face)
            else:
                print("Face already in database - ", face_name)
                cv2.putText(frame, face_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36,255,12), 2)

        # Display the frame with detected faces
        cv2.imshow('Video Stream', frame)
        cv2.waitKey(1)

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()