import gradio as gr
import requests

# Função que chama o endpoint /gerar-imagem
def chamar_api(prompt):
    url = "http://backend-image:9001/gerar-imagem"  # <-- nome do serviço + porta interna
    try:
        response = requests.get(url, params={"prompt_texto": prompt})
        if response.status_code == 200:
            dados = response.json()

            imagem_url = dados.get("imagem_url", "")
            # caracteristicas = dados.get("caracteristicas", [])
            # objetos = dados.get("objetos", [])

            # HTML para exibir imagem
            html_imagem = f"""
                <img src="{imagem_url}" alt="Imagem gerada" width="100%" 
                     style="border: 2px solid #000; border-radius: 10px; margin-top: 10px;">
            """

            # if caracteristicas:
            #     caracteristicas_formatadas = "<ul class='conteudo'>" + "".join(
            #         f"<li>{item['nome']} – {item['confianca']}</li>" for item in caracteristicas
            #     ) + "</ul>"
            # else:
            #     caracteristicas_formatadas = "<p class='conteudo'>Nenhuma característica detectada.</p>"

            # if objetos:
            #     objetos_formatados = "<ul class='conteudo'>" + "".join(
            #         f"<li>{item['nome']} – {item['confianca']}</li>" for item in objetos
            #     ) + "</ul>"
            # else:
            #     objetos_formatados = "<p class='conteudo'>Nenhum objeto detectado.</p>"

            return html_imagem

        else:
            return "<p class='conteudo'>❌ Erro ao gerar imagem</p>", "Erro", "Verifique o servidor da API."
    except Exception as e:
        return f"<p class='conteudo'>❌ Falha: {str(e)}</p>", "Erro", "Erro inesperado"


def build_ui():
    with gr.Blocks(css="""
    #titulo {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        color: #0d6efd;
    }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #000000;
        max-width: 600px;
        margin: 0 auto;
    }
    .gr-button {
        background-color: #0d6efd !important;
        color: white !important;
        border-radius: 8px;
        margin-top: 10px;
        width: 120px;
    }
    .label {
        font-weight: bold;
        margin-top: 16px;
        color: #000000;
    }
    .conteudo {
        color: #000000;
        margin-top: 6px;
    }
    """) as demo:

        gr.HTML('<div id="titulo">AzureLens</div>')

        with gr.Column(elem_classes="card"):
            entrada_texto = gr.Textbox(
                label="💬 Texto:",
                placeholder="Escreva algo criativo...",
                lines=1,
                max_lines=1,
                scale=1
            )

            botao_enviar = gr.Button("Gerar")

            imagem_html = gr.HTML("<p class='conteudo'>Imagem ainda não gerada.</p>")

            # gr.Markdown('<div class="label">🔹 Características:</div>')
            # caracteristicas_texto = gr.HTML("<div class='conteudo'>Ainda não processado.</div>")

            # gr.Markdown('<div class="label">🔹 Objetos Detectados:</div>')
            # objetos_texto = gr.HTML("<div class='conteudo'>Ainda não processado.</div>")

            botao_enviar.click(
                fn=chamar_api,
                inputs=entrada_texto,
                #outputs=[imagem_html, caracteristicas_texto, objetos_texto]
                outputs=[imagem_html]
            )

    return demo

if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860, show_api=False)