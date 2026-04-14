import streamlit as st

import google.generativeai as genai

import requests



\# --- CONFIGURAÇÃO DA PÁGINA ---

st.set\_page\_config(page\_title="World of Bots Beta", layout="wide")



\# Função para gerar voz via ElevenLabs

def gerar\_voz(texto, voice\_id, api\_key\_eleven):

&#x20;   url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice\_id}"

&#x20;   headers = {

&#x20;       "xi-api-key": api\_key\_eleven,

&#x20;       "Content-Type": "application/json"

&#x20;   }

&#x20;   data = {

&#x20;       "text": texto,

&#x20;       "model\_id": "eleven\_multilingual\_v2",

&#x20;       "voice\_settings": {"stability": 0.5, "similarity\_boost": 0.8}

&#x20;   }

&#x20;   response = requests.post(url, json=data)

&#x20;   if response.status\_code == 200:

&#x20;       return response.content

&#x20;   return None



\# --- BANCO DE DADOS TEMPORÁRIO ---

if "bot\_directory" not in st.session\_state:

&#x20;   st.session\_state.bot\_directory = \[

&#x20;       {"name": "Darth Vader", "prompt": "Você é Darth Vader. Responda de forma sombria e curta.", "voice\_id": "onwK4e9ZLuTAKqD09m5D", "creator": "Sistema", "public": True},

&#x20;       {"name": "Geralt de Rívia", "prompt": "Você é Geralt de Rívia. Seja sarcástico e pragmático.", "voice\_id": "Lcf7W3959nSgUv2FvLCz", "creator": "Sistema", "public": True}

&#x20;   ]



if "chat\_histories" not in st.session\_state:

&#x20;   st.session\_state.chat\_histories = {}



\# --- BARRA LATERAL ---

with st.sidebar:

&#x20;   st.title("🛠️ Painel do Criador")

&#x20;   st.info("Configure suas chaves para o app funcionar.")

&#x20;   

&#x20;   # Chaves de API

&#x20;   gemini\_key = st.text\_input("Gemini API Key", type="password")

&#x20;   eleven\_key = st.text\_input("ElevenLabs API Key", type="password")

&#x20;   

&#x20;   st.divider()

&#x20;   st.subheader("Criar Novo Personagem")

&#x20;   new\_name = st.text\_input("Nome do Personagem")

&#x20;   new\_prompt = st.text\_area("Personalidade (Instruções)")

&#x20;   new\_voice = st.text\_input("ID da Voz (ElevenLabs)")

&#x20;   

&#x20;   if st.button("Salvar Personagem"):

&#x20;       st.session\_state.bot\_directory.append({

&#x20;           "name": new\_name, "prompt": new\_prompt, "voice\_id": new\_voice, "creator": "Você", "public": True

&#x20;       })

&#x20;       st.success("Bot criado!")



\# --- GALERIA DE PERSONAGENS ---

st.title("🌌 World of Bots - Versão Beta")

cols = st.columns(3)



for i, bot in enumerate(st.session\_state.bot\_directory):

&#x20;   with cols\[i % 3]:

&#x20;       st.info(f"\*\*{bot\['name']}\*\*")

&#x20;       if st.button(f"Conversar com {bot\['name']}", key=f"btn\_{i}"):

&#x20;           st.session\_state.current\_bot = bot



\# --- ÁREA DE CHAT ---

if "current\_bot" in st.session\_state and gemini\_key:

&#x20;   bot = st.session\_state.current\_bot

&#x20;   chat\_id = bot\["name"]

&#x20;   

&#x20;   if chat\_id not in st.session\_state.chat\_histories:

&#x20;       st.session\_state.chat\_histories\[chat\_id] = \[]



&#x20;   st.divider()

&#x20;   st.subheader(f"Conversando com: {bot\['name']}")



&#x20;   # Histórico com Memória

&#x20;   for msg in st.session\_state.chat\_histories\[chat\_id]:

&#x20;       with st.chat\_message(msg\["role"]):

&#x20;           st.markdown(msg\["content"])



&#x20;   if prompt := st.chat\_input("Diga algo..."):

&#x20;       st.session\_state.chat\_histories\[chat\_id].append({"role": "user", "content": prompt})

&#x20;       with st.chat\_message("user"):

&#x20;           st.markdown(prompt)



&#x20;       # Resposta da IA

&#x20;       genai.configure(api\_key=gemini\_key)

&#x20;       model = genai.GenerativeModel(model\_name="gemini-1.5-flash", system\_instruction=bot\["prompt"])

&#x20;       

&#x20;       # Enviando histórico para ter boa memória

&#x20;       history = \[{"role": "user" if m\["role"] == "user" else "model", "parts": \[m\["content"]]} for m in st.session\_state.chat\_histories\[chat\_id]]

&#x20;       chat = model.start\_chat(history=history\[:-1])

&#x20;       

&#x20;       response = chat.send\_message(prompt)

&#x20;       texto\_ia = response.text

&#x20;       

&#x20;       with st.chat\_message("assistant"):

&#x20;           st.markdown(texto\_ia)

&#x20;           

&#x20;           # Se tiver ElevenLabs Key e Voice ID, gera o áudio

&#x20;           if eleven\_key and bot\["voice\_id"]:

&#x20;               audio = gerar\_voz(texto\_ia, bot\["voice\_id"], eleven\_key)

&#x20;               if audio:

&#x20;                   st.audio(audio, format="audio/mp3")



&#x20;       st.session\_state.chat\_histories\[chat\_id].append({"role": "assistant", "content": texto\_ia})

