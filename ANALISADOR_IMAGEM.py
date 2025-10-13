import streamlit as st
import pandas 

from openai import OpenAI
import base64
import openai
import matplotlib.pyplot as plt 
from PIL import Image
from io import BytesIO

apinumber='sua chave aqui'

client = OpenAI(api_key=apinumber)

def descricao_fruta_bytes(file_bytes):

    imagem64 = base64.b64encode(file_bytes).decode("utf-8")
    prompt="""
    Descreva a imagem com o alimento em questão que aparece em destaque. Se você não verificar nenhum alimento, resposta: "Não identifiquei nenhum alimento". 

    Se a imagem contiver um alimento, faça a seguinte analise: 

    1. Verifique se o alimento está propria para venda. Voce deve considerar: 
    1.1. Injurias
    1.2 Ponto de maturação
    1.3 Podridão
    1.4 Presença de fungos ou outro microorganismos que reduzam ou causem descomprimento a qualidade propria de venda do produto em questão. 

    2. Na sua analise analise considere a quantidade de alimento na foto. Faça uma descrição dos alimentos e sua quantidade aproximada. 

    3. Desconsidere o ambiente ao redor. Foque nos alimentos mostrados na imagem. 

    4. Construa seu texto de forma resumida e objetiva. Voce pode utilizar emoji para facilitar a leitura pelo leitor. 
    
    No final do seu relatorio, coloque em destaque, algo similar como: "O ALIMENTO ESTA IMPROPRIO PARA VENDA", ou "O ALIMENTO ESTA EM BOAS CONDICOES PARA VENDA" ou "A MAIORIA ESTA EM BOAS CONDICOES PARA VENDA" ou "A MAIORIA ESTA IMPROPRIA PARA VENDA". Considere adaptar o texto caso necessario citando os alimentos em questão, sua quantidade e alertas a condicoes de venda.  
    
    """

    messages_lista = [
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
                {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagem64}"}}]}
            ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",        
        messages=messages_lista,
        n=1,temperature=1.0
    )
    return response.choices[0].message.content
    
    
# --- Interface Streamlit ---
st.title("🍎 Análise de FLV do Super do POVO")


image = Image.open('imagem_frutas/logosp.jpeg')
st.image(image, caption="Super do povo - Supermercado")

if st.button("🔄 Atualizar imagem"):
    st.rerun()

opcao = st.radio("Escolha como enviar a imagem:", ["📂 Upload de arquivo", "📷 Usar câmera"])

file_bytes = None

if opcao == "📂 Upload de arquivo":
    uploaded_file = st.file_uploader("Envie uma imagem:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()

elif opcao == "📷 Usar câmera":
    camera_file = st.camera_input("Tire uma foto")
    if camera_file is not None:
        file_bytes = camera_file.getvalue()

# Se recebeu alguma imagem (por upload ou câmera)
if file_bytes is not None:
    image = Image.open(BytesIO(file_bytes))
    st.image(image, caption="Imagem recebida")

    if st.button("Analisar alimento"):
        with st.spinner("Analisando a imagem..."):
            resultado = descricao_fruta_bytes(file_bytes)
            st.success("✅ Análise concluída!")
            st.write(resultado)
    
    

