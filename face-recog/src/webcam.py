import sys
from face_detection import detect_faces
from utils import load_config
from database import Database
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import gradio as gr
import logging
import dlib

def inference(input_img):
    output_img = input_img  # Placeholder for processed image

    # Detect faces in the input image
    faces = detect_faces(input_img)

    for face in faces:
        face_name=database.face_is_in_database(face)
            
        if face_name is None:
            # print("New face detected - inserting into database") 
            database.insert_face_in_database(face)
        else:
            # print("Face already in database - ", face_name)
            # Draw rectangles around detected face and write the name of the person
            x, y, w, h = face[1]
            if face_name == "Unknown":
                pen_color = "red"
            else:
                pen_color = "green"

            draw = ImageDraw.Draw(output_img)    
            width_size = 7
            draw.rectangle([(x, y), (x+w, y+h)], outline=pen_color, width=width_size)
            font_size=50
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=font_size)
            draw.text((x, y - font_size*1.2), text=str(face_name), fill=pen_color, font=font)
            
    return output_img


# Gradio UI setup / (Web page)
css="body{background-color: #f5f4f2; --body-background-fill: #f5f4f2} footer{display:none !important}"

with gr.Blocks(title='Face Recognition Demo') as demo:
    gr.set_static_paths(paths=["cont/images/"])
    #gr.HTML("<img src='cont/images/OSC.png'>")
    gr.Markdown("![](gradio_api/file=images/OSC.png)")
    gr.Markdown("<center><h1>Face Recognition Demo</h1></center>")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type='pil', label='Input Image', sources=['webcam'], streaming=True,show_label=False)
        with gr.Column():
            output_img = gr.Image(type='pil', label='Output Image',buttons=['fullscreen','download'], show_label=False)

    dep = input_img.stream(inference, inputs=[input_img], outputs=[output_img], stream_every=1)
    # stream=0.5 doesn't work 

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Starting Face Recognition Demo (webcam)...")

    logging.debug("dlib.DLIB_USE_CUDA =" + str(dlib.DLIB_USE_CUDA)) # Must be True
    logging.debug("dlib.cuda.get_num_devices() =" + str(dlib.cuda.get_num_devices())) # Must be > 0

    # Load configuration
    config = load_config()

    # Initialize the database
    database = Database(config["database_config"]["username"], config["database_config"]["password"])
    database.connect()

    # Gradio hides output sometimes, so we force flush here
    sys.stdout.flush()

    # Launch the Gradio app
    demo.launch(debug=True, share=False, server_port=8443, server_name='0.0.0.0',
                css=css,
                root_path="/app", auth=("demo", "aicec"),
                allowed_paths=["images/"])
    
