import gradio as gr
import requests
import json

# Comentário para atualização do repositório
def envia(json_text):
    objeto_json = json.loads(json_text)
    url ="http://backend-json:8080/json/"
    r = requests.post(url, json=objeto_json)
    return r.content

demo = gr.Interface(fn=envia, inputs="text",outputs="text")

if __name__ == "__main__":
    demo.launch(server_name ="0.0.0.0", server_port=7860,show_api=False)

