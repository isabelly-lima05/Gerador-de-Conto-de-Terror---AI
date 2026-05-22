# app.py
import os
import json
from flask import Flask, jsonify, request, Response, stream_with_context
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

# Lista de palavras-chave restritas para triagem rápida local
PALAVRAS_PROIBIDAS = [
    "suicidio", "autoflagelacao", "automutilacao", "como fazer bomba", 
    "estupro", "pedofilia", "gilete", "enforcar"
]

def generate_horror_stream(cenario, tipo_medo, estilo_escrita):
    conteudo_prompt = f"""
    Escreva um conto de terror psicológico com as seguintes características:
    - Cenário de Isolamento: {cenario}
    - Tipo de Medo/Ameaça: {tipo_medo}
    - Estilo Narrativo: {estilo_escrita}
    """
    
    try:
        response_stream = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=conteudo_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=CONTO_SCHEMA,
                temperature=0.85,
            )
        )
        
        for chunk in response_stream:
            if chunk.text:
                # Formatação padrão do protocolo Server-Sent Events (SSE)
                yield f"data: {chunk.text}\n\n"
                
    except APIError as e:
        # Envia uma resposta JSON de erro estruturada dentro do stream caso a API falhe (ex: erro 503)
        error_payload = json.dumps({
            "status": "error",
            "message": f"Erro de comunicação com o provedor de IA (Código {e.code}). Tente novamente em breve."
        })
        yield f"data: {error_payload}\n\n"
        
    except Exception as e:
        error_payload = json.dumps({
            "status": "error",
            "message": f"Erro inesperado durante a transmissão: {str(e)}"
        })
        yield f"data: {error_payload}\n\n"

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Gerador de Contos de Terror Ativa!",
        "version": "1.1",
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
            "message": "Preencha todos os campos obrigatórios: cenario, tipo_medo, estilo_escrita."
        }), 400
    
    # Camada de Proteção Local
    texto_combinado = f"{cenario} {tipo_medo} {estilo_escrita}".lower()
    if any(palavra in texto_combinado for palavra in PALAVRAS_PROIBIDAS):
        return jsonify({
            "status": "error",
            "message": "Sua solicitação contém termos restritos por nossas políticas de segurança."
        }), 400
            
    try:
        # O uso de stream_with_context garante o gerenciamento de recursos do Flask durante o SSE
        return Response(
            stream_with_context(generate_horror_stream(cenario, tipo_medo, estilo_escrita)),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Transfer-Encoding': 'chunked',
                'Connection': 'keep-alive'
            }
        )
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Não foi possível iniciar o serviço de geração: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)