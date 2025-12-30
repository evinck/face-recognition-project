import sys
from face_detection import detect_faces
from utils import load_config
from database import Database
from datetime import datetime
from PIL import Image, ImageDraw
import gradio as gr
import logging
import pickle

def update_face_name(id,new_name):
    database.update_face_name_in_database(face_id=id, new_name=new_name)
    return new_name

def delete_face(id):
    database.delete_face_from_database(face_id=id)
    return refresh_faces()

def refresh_faces():
    return database.faces_from_database()
  
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting Face Recognition Demo...")

    # Load configuration
    config = load_config()

    # Initialize the database
    database = Database(config["database_config"]["username"], config["database_config"]["password"])
    database.connect()

    # Gradio UI setup / (Web page)
    css="body{background-color: #f5f4f2; --body-background-fill: #f5f4f2} footer{display:none !important}"

    with gr.Blocks(title='Face Recognition Demo') as demo:
        gr.set_static_paths(paths=["cont/images/"])
        #gr.HTML("<img src='cont/images/OSC.png'>")
        gr.Markdown("![](gradio_api/file=images/OSC.png)")
        gr.Markdown("<center><h1>Face Recognition Demo</h1></center>")
    
        faces_state = gr.State(refresh_faces)

        @gr.render(inputs=[faces_state])
        def display_faces(faces):
            for face in faces:
                image= face[1]
                with gr.Row():
                    with gr.Column():
                        gr.Image(value=image, height=200, width=200, buttons=['fullscreen'], show_label=False)
                    with gr.Column():
                        textbox = gr.Textbox(placeholder=str(face[2]), value=str(face[2]), label="Name",interactive=True)
                        textbox.submit(fn=update_face_name, inputs=[gr.State(face[0]), textbox], outputs=[textbox])
                    with gr.Column():
                        with gr.Row():
                            submit_btn = gr.Button("Update Name",variant="primary")
                            submit_btn.click(fn=update_face_name, inputs=[gr.State(face[0]), textbox], outputs=[textbox])
                        with gr.Row():
                            delete_btn = gr.Button("Delete Face", variant="stop")
                            delete_btn.click(fn=delete_face, inputs=[gr.State(face[0])], outputs=[faces_state])

        update_faces_btn = gr.Button("Update Faces",variant="primary")
        update_faces_btn.click(fn=refresh_faces, inputs=[], outputs=[faces_state])

    # Launch the Gradio app
    demo.launch(debug=True, share=False, server_port=8444, server_name='0.0.0.0',
                css=css,
                root_path="/app", auth=("demo", "aicec"),
                allowed_paths=["images/"])

