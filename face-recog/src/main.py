from face_detection import detect_faces
from utils import load_config
from database import Database
from datetime import datetime
from PIL import Image, ImageDraw
import gradio as gr


def inference(input_img):
    output_img = input_img  # Placeholder for processed image

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
                pen_color = 'red'
            else:
                pen_color = 'green'

            draw = ImageDraw.Draw(output_img)    
            draw.rectangle([(x, y), (x+w, y+h)], outline=pen_color, width=2)
            draw.text((x, y-10), text=str(face_name), fill=pen_color)   

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
            input_img = gr.Image(type='pil', label='Input Image', sources=['webcam'], streaming=True)
        with gr.Column():
            output_img = gr.Image(type='pil', label='Output Image')
        with gr.Column():
            button = gr.Button("Clean All")

    dep = input_img.stream(inference, inputs=[input_img], outputs=[output_img], stream_every=0.1)

if __name__ == '__main__':
    print("Starting Face Recognition Demo...",flush=True)

    # Load configuration
    config = load_config()

    # Initialize the database
    database = Database(config["database_config"]["username"], config["database_config"]["password"])
    database.connect()

    # Launch the Gradio app
    demo.launch(debug=True, share=False, server_port=8443, server_name='0.0.0.0',
                css=css,
                root_path="/app", auth=("demo", "aicec"),
                allowed_paths=["images/"])
