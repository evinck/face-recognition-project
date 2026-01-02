import cx_Oracle
import pickle
import logging

class Database:
    def __init__(self, user, password, ctx_string):
        self.user = user
        self.password = password
        self.ctx_string = ctx_string
        self.connection = None

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(
                self.user, self.password, dsn=self.ctx_string)
            logging.info("Database connection established.")
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error connecting to database: {e}")

    # inserts a face into the database
    def insert_face_in_database(self, face):
        if self.connection is None:
            logging.info("Database connection is not established.")
            return

        cursor = self.connection.cursor()
        try:
            # ORA-24816 Error if face_image is not the last parameter
            # cursor.execute("INSERT INTO faces (face_image, face_name, face_vector) VALUES (:1, :2, :3)", [pickle.dumps(face[0]), "Unknown", str(face[2].tolist())])
            cursor.execute("INSERT INTO faces (face_name, face_vector, face_image) VALUES (:1, :2, :3)", ["Unknown", str(face[2].tolist()), pickle.dumps(face[0])])
            self.connection.commit()
            logging.info("Face inserted successfully.")
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error inserting face: {e}")
        finally:
            cursor.close()

    # returns the name of the face if it is in the database, otherwise returns an empty string
    def face_is_in_database(self, face):
        if self.connection is None:
            logging.info("Database connection is not established.")
            return False

        cursor = self.connection.cursor()
        try:
            # Cosine Distance varies from 0 to 2, where 0 means the vectors are identical and 2 means they are opposite
            distance_threshold = 0.55
            cursor.execute(""" 
                SELECT face_name FROM faces 
                WHERE VECTOR_DISTANCE(face_vector, :parameter_vector, COSINE) <= :distance_threshold
                ORDER BY VECTOR_DISTANCE(face_vector, :parameter_vector, COSINE)
                ASC FETCH FIRST 1 ROW ONLY""", [str(face[2].tolist()), distance_threshold])
            row = cursor.fetchone()
            if row is not None:
                return str(row[0])
            else:
                return None
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error checking if face is in database: {e}")
        finally:
            cursor.close()

    # returns n (how_many) or all (when how_many=None) faces (id, name, image) from the database
    def faces_from_database(self, how_many=None):
        if self.connection is None:
            logging.info("Database connection is not established.")

        cursor = self.connection.cursor()
        try:
            if how_many is None:
                cursor.execute(
                    "SELECT id, face_image, face_name FROM faces")
            else:
                cursor.execute(
                    "SELECT id, face_image, face_name FROM faces FETCH FIRST :1 ROWS ONLY", [how_many])
            rows = cursor.fetchall()
            faces = []
            for row in rows:
                face = (row[0],  pickle.loads(row[1].read()), row[2])
                faces.append(face)
            return faces      
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error fetching faces: {e}")
        finally:
            cursor.close()

    def empty_database(self, filter_name=None):
        if self.connection is None:
            logging.info("Database connection is not established.")

        try:
            cursor = self.connection.cursor()
            if filter_name is None:
                cursor.execute("TRUNCATE table faces")
                self.connection.commit()
                logging.info("Database emptied successfully.")
            else:
                cursor.execute("DELETE FROM faces where face_name = :1", [filter_name])
                self.connection.commit()
                logging.info(f"All faces deleted with filer = {filter_name } successfully.")
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error deleting database: {e}")
        finally:
            cursor.close()

    def update_face_name_in_database(self, face_id, new_name):
        if self.connection is None:
            print("Database connection is not established.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE faces SET face_name = :1 WHERE id = :2", [new_name, face_id])
            self.connection.commit()
            logging.info(f"Face name updated successfully.")
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error updating face name: {e}")
        finally:
            cursor.close()

    def delete_face_from_database(self, face_id):
        if self.connection is None:
            logging.info("Database connection is not established.")

        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM faces WHERE id = :1", [face_id])
            self.connection.commit()
            logging.info(f"Face deleted successfully.")
        except cx_Oracle.DatabaseError as e:
            logging.info(f"Error deleting face: {e}")
        finally:
            cursor

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")
