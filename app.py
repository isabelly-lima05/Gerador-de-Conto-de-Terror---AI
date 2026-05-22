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
                yield f"data: {chunk.text}\n\n"
                
    except APIError as e:
        # ensure_ascii=False garante a codificação correta de acentos em UTF-8 no stream
        error_payload = json.dumps({
            "status": "error",
            "message": "Ruído no Éter: O repositório central de ideias está sob alta demanda ou temporariamente indisponível. O silêncio responde por agora. Tente invocar a prosa novamente em instantes."
        }, ensure_ascii=False)
        yield f"data: {error_payload}\n\n"
        
    except Exception as e:
        error_payload = json.dumps({
            "status": "error",
            "message": "Anomalia Narrativa: Uma interferência desconhecida corrompeu o fluxo da escrita. Verifique as configurações de rede e tente projetar a prosa novamente."
        }, ensure_ascii=False)
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
            "message": "Parâmetros incompletos. Forneça o cenário, tipo de medo e estilo de escrita para iniciar."
        }), 400
    
    # Camada de Proteção Local
    texto_combinado = f"{cenario} {tipo_medo} {estilo_escrita}".lower()
    if any(palavra in texto_combinado for palavra in PALAVRAS_PROIBIDAS):
        return jsonify({
            "status": "error",
            "message": "Sinal Interrompido: A frequência de ideias sugeridas ultrapassa as barreiras de nossa moderação de segurança. O terror psicológico evoca o mistério e a paranoia, evitando a violência física explícita."
        }), 400
            
    try:
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
            "message": f"Não foi possível iniciar o serviço de geração de texto: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)