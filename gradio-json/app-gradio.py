import gradio as gr
import requests
import json

def envia(json_text):
    objeto_json = json.loads(json_text)
    return objeto_json

demo = gr.Interface(fn=envia, inputs="text",outputs="text")

if __name__ == "__main__":
    demo.launch(server_name ="0.0.0.0", server_port=7860,show_api=False)

