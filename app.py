# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

from config import CONTO_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicialização do cliente Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

# Lista de palavras-chave restritas para segurança local rápida
PALAVRAS_PROIBIDAS = [
    "suicidio", "autoflagelacao", "automutilacao", "como fazer bomba", 
    "estupro", "pedofilia", "gilete", "enforcar"
]

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Gerador de Contos de Terror Ativa!",
        "version": "1.3",
        "author": "Isabelly"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Parâmetros ausentes no corpo da requisição."}), 400
        
    cenario = data.get("cenario", "").strip()
    tipo_medo = data.get("tipo_medo", "").strip()
    estilo_escrita = data.get("estilo_escrita", "").strip()
    
    if not cenario or not tipo_medo or not estilo_escrita:
        return jsonify({
            "status": "error", 
            "message": "Parâmetros incompletos. Forneça o cenário, tipo de medo e estilo de escrita."
        }), 400
    
    # Camada de Proteção Local (Filtro Rápido)
    texto_combinado = f"{cenario} {tipo_medo} {estilo_escrita}".lower()
    if any(palavra in texto_combinado for palavra in PALAVRAS_PROIBIDAS):
        return jsonify({
            "status": "error",
            "message": "Sinal Interrompido: A frequência de ideias sugeridas ultrapassa as barreiras de nossa moderação de segurança. O terror psicológico evoca o mistério e a paranoia, evitando a violência física explícita."
        }), 400
            
    conteudo_prompt = f"""
    Escreva um conto de terror psicológico com as seguintes características:
    - Cenário de Isolamento: {cenario}
    - Tipo de Medo/Ameaça: {tipo_medo}
    - Estilo Narrativo: {estilo_escrita}
    """
    
    try:
        # Chamada direta com configurações de segurança permissivas para escrita criativa
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=conteudo_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=CONTO_SCHEMA,
                temperature=0.85,
                # Ajuste de filtros para evitar falsos positivos em escrita de suspense
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                ]
            )
        )
        
        # Converte a resposta de texto (JSON) de volta para um dicionário Python
        conto_json = json.loads(response.text)
        
        return jsonify({
            "status": "success",
            "dados_conto": conto_json
        }), 200
        
    except APIError as e:
        # Retorna a mensagem de erro detalhada da API para facilitar o diagnóstico
        return jsonify({
            "status": "error",
            "message": f"Ruído no Éter (Erro {e.code}): {e.message}"
        }), 503
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Anomalia Narrativa: Erro no processamento do conto. {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)