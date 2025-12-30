import tkinter as tk
from tkinter import ttk
import threading
from database import Database
from PIL import Image, ImageTk
import io
import time

class Editor:
    def __init__(self, database):
        self.database = database
        self.fps = 0
        # FPS display label
        self.fps_label = None

    def set_fps(self, fps):
        self.fps = fps  # Update the FPS value
        if self.fps_label is not None:
            self.fps_label.config(text=f"FPS:  {self.fps:.2f}")  # Update the label

    def start_text_editor_thread(self):
        editor_thread = threading.Thread(target=self.open_text_editor)
        editor_thread.daemon = True
        editor_thread.start()

    def open_text_editor(self):
        # Create a Tkinter window
        root = tk.Tk()
        root.title("Face Editor")

        # Create a Canvas widget with a scrollbar
        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # Create a Frame to display faces inside the scrollable frame
        faces_frame = tk.Frame(scrollable_frame)
        faces_frame.pack(padx=20, pady=20)

        # Create a Scale widget to choose a value between 0.0 and 2.0
        scale_frame = tk.Frame(root)
        scale_frame.pack(padx=20, pady=20)

        scale = tk.Scale(scale_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Distance Threshold")
        scale.pack(side=tk.LEFT)

        def set_threshold():
            self.database.distance_threshold = float(scale.get())
            print(f"Distance threshold set to: {self.database.distance_threshold}")

        set_button = tk.Button(scale_frame, text="Set", command=set_threshold)
        set_button.pack(side=tk.RIGHT, padx=10)

        # Refresh the list of faces
        def refresh():
            for widget in faces_frame.winfo_children():
                widget.destroy()  # Clear the frame

            faces = self.database.faces_from_database(10)  # Fetch faces from the database
            for face in faces:
                # Display face[0] as an image
                image_data = face[2]
                image = Image.fromarray(image_data)
                # image = image.resize((100, 100), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(faces_frame, image=photo)
                image_label.image = photo  # Keep a reference to avoid garbage collection
                image_label.pack()

                # Create an Entry widget to display face[1] as text
                text_widget = tk.Entry(faces_frame, width=30)
                text_widget.insert(tk.END, f"{face[1]}")
                text_widget.pack()

                def update_face_name(face_id, text_widget):
                    new_name = text_widget.get().strip()
                    self.database.update_face_name(face_id, new_name)
                    print(f"Updated face ID {face_id} with new name: {new_name}")

                update_button = tk.Button(faces_frame, text="Update Name", command=lambda face_id=face[0], text_widget=text_widget: update_face_name(face_id, text_widget))
                update_button.pack()

                def delete_face(face_id):
                    self.database.delete_face(face_id)
                    refresh()
                    print(f"Deleted face ID {face_id}")

                delete_button = tk.Button(faces_frame, text="Delete", command=lambda face_id=face[0]: delete_face(face_id))
                delete_button.pack()

        # Periodically refresh the list of faces
        # doesn't work as intended
        # def periodic_refresh():
        #     while True:
        #         time.sleep(3)
        #         refresh()

        # refresh_thread = threading.Thread(target=periodic_refresh)
        # refresh_thread.daemon = True
        # not starting because of consequences
        # refresh_thread.start()

        # Refresh button to call the refresh function "manually"
        refresh_button = tk.Button(root, text="Refresh list", command=refresh)
        refresh_button.pack(pady=10)

        # Create a button to empty the database
        def empty_database():
            self.database.empty_database()
            refresh()

        empty_button = tk.Button(root, text="Empty database", command=empty_database)
        empty_button.pack(pady=10)

        # Display the FPS value
        self.fps_label = tk.Label(root, text=f"FPS:  {self.fps:.2f}")
        self.fps_label.pack(pady=10)

        # Run the Tkinter event loop
        root.mainloop()

if __name__ == "__main__":
    # Initialize the database
    database = Database("your_username", "your_password")
    database.connect()

    # Start the editor
    editor = Editor(database)
    editor.start_text_editor_thread()

    # Example of other code running in parallel
    while True:
        print("Main application running...")
        time.sleep(1)





