import cx_Oracle
import pickle


class Database:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.connection = None
        self.distance_threshold = 0.1

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(
                self.user, self.password, dsn="db:1521/FREEPDB1")
            print("Database connection established.")
        except cx_Oracle.DatabaseError as e:
            print(f"Error connecting to database: {e}")

    # inserts a face into the database
    def insert_face_in_database(self, face):
        if self.connection is None:
            print("Database connection is not established.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO faces (face_image, face_name, face_vector) VALUES (:1, :2, :3)", [pickle.dumps(face[0]), "Unkown", str(face[2].tolist())])
            self.connection.commit()
            print("Face inserted successfully.")
        except cx_Oracle.DatabaseError as e:
            print(f"Error inserting face: {e}")
        finally:
            cursor.close()

    # returns the name of the face if it is in the database, otherwise returns an empty string
    def face_is_in_database2(self, face):
        if self.connection is None:
            print("Database connection is not established.")
            return False

        cursor = self.connection.cursor()
        try:
            # Cosine Distance varies from 0 to 2, where 0 means the vectors are identical and 2 means they are opposite
            result = ""
            cursor.execute(""" 
                SELECT face_name FROM faces 
                WHERE VECTOR_DISTANCE(face_vector, :parameter_vector, COSINE) <= :distance_threshold
                ORDER BY VECTOR_DISTANCE(face_vector, :parameter_vector, COSINE)
                ASC FETCH FIRST 1 ROW ONLY""", [str(face[2].tolist()), self.distance_threshold])
            row = cursor.fetchone()
            if row is not None:
                result = row[0]
            return result
        except cx_Oracle.DatabaseError as e:
            print(f"Error checking if face is in database: {e}")
        finally:
            cursor.close()

    # returns n (how_many) faces (id, image, name) from the database
    def faces_from_database(self, how_many):
        if self.connection is None:
            print("Database connection is not established.")

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, face_image, face_name FROM faces FETCH FIRST :1 ROWS ONLY", [how_many])
            rows = cursor.fetchall()
            faces = []
            for row in rows:
                # face = (row[0], pickle.loads(row[1]), row[2])
                face = (row[0], row[2])
                faces.append(face)
            return faces      
        except cx_Oracle.DatabaseError as e:
            print(f"Error inserting face: {e}")
        finally:
            cursor.close()

    def empty_database(self):
        if self.connection is None:
            print("Database connection is not established.")

        try:
            cursor = self.connection.cursor()
            cursor.execute("TRUNCATE table faces")
            print("Database emptied successfully.")
        except cx_Oracle.DatabaseError as e:
            print(f"Error inserting face: {e}")
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
