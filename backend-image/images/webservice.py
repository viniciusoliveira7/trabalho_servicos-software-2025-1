import requests
import json
from openai import AzureOpenAI
import os
from os import path
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
assets_path = os.getcwd() + "/swagger-ui-assets"

if path.exists(assets_path + "/swagger-ui.css") and path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")

    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )

    applications.get_swagger_ui_html = swagger_monkey_patch


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"

def traduzir_texto(texto, idioma_destino="pt"):
    translator_endpoint = os.getenv("TRANSLATOR_ENDPOINT")
    translator_key = os.getenv("TRANSLATOR_KEY")
    translator_location = os.getenv("TRANSLATOR_LOCATION")

    url = f"{translator_endpoint}translate?api-version=3.0&to={idioma_destino}"
    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": translator_location,
        "Content-Type": "application/json"}

    body = [{"text": texto}]
    response = requests.post(url, headers=headers, json=body)

    return response.json()[0]["translations"][0]["text"]

@app.get("/gerar-imagem", tags=["Endpoints"])
async def gerar_imagem(prompt_texto):
  azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
  azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
  azure_openai_version = os.getenv("AZURE_OPENAI_VERSION")

  client = AzureOpenAI(
      api_version=azure_openai_version,
      azure_endpoint=azure_openai_endpoint,
      api_key=azure_openai_key)

  result = client.images.generate(
      model="dall-e-3",
      prompt=prompt_texto,
      quality="hd",
      n=1)

  imagem_gerada = json.loads(result.model_dump_json())['data'][0]['url']

  #resultado_analise = await analisar_imagem(imagem_gerada)

  #return resultado_analise

  return {
            "imagem_url": imagem_gerada
        }


# async def analisar_imagem(imagem_url):
#     computer_vision_endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")
#     computer_vision_key = os.getenv("COMPUTER_VISION_KEY")
#     caracteristicas = []
#     objetos = []

#     analyze_url = computer_vision_endpoint + "/vision/v3.2/analyze"

#     # Baixa a imagem via GET
#     image_data = requests.get(imagem_url).content

#     headers = {"Ocp-Apim-Subscription-Key": computer_vision_key, "Content-Type": "application/octet-stream"}
#     params = {"visualFeatures": "Tags,Objects"}
        
#     response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
#     response.raise_for_status()
#     analysis = response.json()
        
#     for tag in analysis.get("tags", []):
#         tag_pt = traduzir_texto(tag["name"])
#         caracteristicas.append({"nome": tag_pt, "confianca": f"{tag['confidence'] * 100:.2f}%"})
        
#     for obj in analysis.get("objects", []):
#         obj_pt = traduzir_texto(obj["object"])
#         objetos.append({
#             "nome": obj_pt,
#             "confianca": f"{obj['confidence'] * 100:.2f}%"
#         })

#     return {
#         "imagem_url": imagem_url,
#         "caracteristicas": caracteristicas,
#         "objetos": objetos
#     }