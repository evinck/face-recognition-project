import tkinter as tk
import threading
from database import Database
import time

class Editor:
    def __init__(self, database):
        self.database = database

    def start_text_editor_thread(self):
        editor_thread = threading.Thread(target=self.open_text_editor)
        editor_thread.daemon = True
        editor_thread.start()

    def open_text_editor(self):
        # Create a Tkinter window
        root = tk.Tk()
        root.title("Face Editor")

        # Create a Text widget to display faces
        text_widget = tk.Text(root, width=50, height=20)
        text_widget.pack(padx=20, pady=20)

        # Create a Scale widget to choose a value between 0.0 and 2.0
        scale_frame = tk.Frame(root)
        scale_frame.pack(padx=20, pady=20)

        scale = tk.Scale(scale_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Distance Threshold")
        scale.pack(side=tk.LEFT)

        def set_threshold():
            self.database.empty_database()
            self.database.distance_threshold = float(scale.get())
            print(f"Distance threshold set to: {self.database.distance_threshold}")

        set_button = tk.Button(scale_frame, text="Set", command=set_threshold)
        set_button.pack(side=tk.LEFT, padx=10)

        # Create a button to refresh the displayed faces
        def refresh():
            text_widget.delete(1.0, tk.END)  # Clear the text widget
            faces = self.database.faces_from_database(10)  # Fetch faces from the database
            for face in faces:
                text_widget.insert(tk.END, f"Face ID: {face[0]} Face Name: {face[1]} \n")

        refresh_button = tk.Button(root, text="Refresh list", command=refresh)
        refresh_button.pack(pady=10)

        # Create a button to empty the database
        empty_button = tk.Button(root, text="Empty database", command=self.database.empty_database)
        empty_button.pack(pady=10)

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





