import sys
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

delete_faces_btn_visible: bool=False
def delete_faces():
    global delete_faces_btn_visible
    global face_choice

    if face_choice=="Unknowns":
        logging.debug("Deleting all Unknown faces from database")
        database.empty_database("Unknown")
        delete_faces_btn_visible=True
    else:
        logging.debug("No faces deleted from database - unrecognized filter")
    
    return refresh_faces()

face_choice="All Faces"
def dropdown_fn(choice):
    global face_choice
    global delete_faces_btn_visible

    logging.debug(f"Dropdown choice changed to: {choice}")
    face_choice=choice

    if face_choice=="Unknowns":
        delete_faces_btn_visible=True
    else :
        delete_faces_btn_visible=False
    
    return refresh_faces()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting Face Recognition Demo (dbutil)...")

    # Load configuration
    config = load_config()

    # Initialize the database
    database = Database(config["database_config"]["username"], config["database_config"]["password"],config["database_config"]["ctx_string"])
    database.connect()

    # Gradio UI setup / (Web page)
    css="body{background-color: #f5f4f2; --body-background-fill: #f5f4f2} footer{display:none !important}"

    with gr.Blocks(title='Face Recognition Demo') as demo:
        gr.set_static_paths(paths=["cont/images/"])
        #gr.HTML("<img src='cont/images/OSC.png'>")
        gr.Markdown("![](gradio_api/file=images/OSC.png)")
        gr.Markdown('<center><div style="width: 100%; background-color: #bf0000; padding: 10px; margin: -10px -10px 10px -10px;"><h2>GDPR compliance : this is a technical demo. We won\'t keep biometric data.</h2></div></center>')
        gr.Markdown("<center><h1>Face Recognition Demo - Database utility</h1></center>")
    
        # Faces list
        faces_state = gr.State(refresh_faces())
        
        # Render faces
        @gr.render(inputs=[faces_state])
        def display_faces(faces):
            global face_choice
            global delete_faces_btn_visible

            # Faces list
            # faces_state = gr.State(refresh_faces())

            with gr.Row():
                dropdown = gr.Dropdown(choices=["All Faces","Unknowns","Knowns"], value=face_choice, label="What faces to display", interactive=True)
                dropdown.change(fn=dropdown_fn, inputs=[dropdown], outputs=[faces_state])
                with gr.Row(variant="compact"):
                    update_faces_btn = gr.Button("Refresh",variant="primary")
                    update_faces_btn.click(fn=refresh_faces, inputs=[], outputs=[faces_state])
                    delete_faces_btn = gr.Button("Delete All",variant="stop", interactive=delete_faces_btn_visible)
                    delete_faces_btn.click(fn=delete_faces, inputs=[], outputs=[faces_state])

            logging.debug(f"Got {len(faces)} faces from database")
            logging.debug(f"Will apply filter: {face_choice}")
            logging.debug(f"Delete faces button visible: {delete_faces_btn_visible}")
            
            for face in faces:
                face_name=face[2]
                if (face_choice=="Unknowns" and face_name=="Unknown") or \
                   (face_choice=="Knowns" and face_name!="Unknown") or \
                     (face_choice=="All Faces"):
                        face_id = face[0]
                        face_image = face[1]
                        with gr.Row():
                            logging.debug(f"Image type: {type(face_image)}")
                            logging.debug(f"Displaying face id={face_id}, name={face_name}, size={face_image.size}")
                            # Weird bug : sometimes face.size.x or y can be 0, causing gr.Image to crash
                            # if face_image.size[0]!=0 and face_image.size[1]!=0:
                            try :
                                gr.Image(value=face_image, height=200, width=200, buttons=['fullscreen'], label=str(face_id))
                            except Exception as e:
                                logging.error(f"Error displaying image for face id={face_id}: {e}")
                                face_image = Image.new('RGB', (200, 200), color = 'red')
                                gr.Image(value=face_image, height=200, width=200, buttons=['fullscreen'], label=str(face_id)+" (error)")
                            textbox = gr.Textbox(placeholder=str(face_name), value=str(face_name), label="Name",interactive=True)
                            textbox.submit(fn=update_face_name, inputs=[gr.State(face[0]), textbox], outputs=[textbox])
                            with gr.Row(variant="compact"):
                                submit_btn = gr.Button("Update Name",size="sm")
                                submit_btn.click(fn=update_face_name, inputs=[gr.State(face[0]), textbox], outputs=[textbox])
                                delete_btn = gr.Button("Delete Face",size="sm")
                                delete_btn.click(fn=delete_face, inputs=[gr.State(face[0])], outputs=[faces_state])


        update_faces_btn = gr.Button("Refresh",variant="primary")
        update_faces_btn.click(fn=refresh_faces, inputs=[], outputs=[faces_state])

    # Launch the Gradio app
    demo.launch(debug=True, share=False, server_port=9444, server_name='0.0.0.0',
                css=css,
                root_path="/dbutil", auth=("demo", "aicec"),
                allowed_paths=["images/"],
                ssl_verify=False,
                ssl_certfile="cert.pem",
                ssl_keyfile="key.pem")


