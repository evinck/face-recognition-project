CREATE TABLE IF NOT EXISTS FACES (
    ID NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
    face_vector VECTOR,
    face_image BLOB,
    face_name VARCHAR2(255) 
);