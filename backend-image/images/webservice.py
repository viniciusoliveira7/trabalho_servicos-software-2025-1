import requests
import json
from openai import AzureOpenAI
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import os
from os import path
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse, JSONResponse
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

async def traduzir_texto(texto, idioma_destino="pt"):
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
      n=1)

  imagem_gerada = json.loads(result.model_dump_json())['data'][0]['url']

  resultado_analise = analisar_imagem(imagem_gerada)

  return resultado_analise


async def analisar_imagem(imagem_url):
  computer_vision_endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")
  computer_vision_key = os.getenv("COMPUTER_VISION_KEY")

  # Criar um cliente de Análise de Imagem
  client = ImageAnalysisClient(endpoint=computer_vision_endpoint, credential=AzureKeyCredential(computer_vision_key))

  # Obter uma análise completa da imagem
  result = client.analyze_from_url(
      image_url=imagem_url,
      visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS],
      gender_neutral_caption=True)

  # Processar características da imagem
  caracteristicas = []
  if result.tags and "values" in result.tags:
      for tag in result.tags["values"]:
          tag_pt = traduzir_texto(tag["name"])
          caracteristicas.append({"nome": tag_pt, "confianca": f"{tag['confidence'] * 100:.2f}%"})
    
  # Processar objetos detectados
  objetos = []
  if result.objects and "values" in result.objects:
      for obj in result.objects["values"]:
          for tag in obj["tags"]:
              obj_pt = traduzir_texto(tag["name"])
              objetos.append({"nome": obj_pt, "confianca": f"{tag['confidence'] * 100:.2f}%"})
  
  return {
      "imagem_url": imagem_url,
      "caracteristicas": caracteristicas,
      "objetos": objetos}