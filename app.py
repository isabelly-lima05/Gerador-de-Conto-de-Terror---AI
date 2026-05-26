# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

from config import DOSSIE_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API de Dossiês Criminais Exaustivos Ativa",
        "version": "2.5"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Corpo da requisição vazio."}), 400
        
    pesquisa = data.get("nome_pesquisa", "").strip()
    
    if not pesquisa:
        return jsonify({
            "status": "error", 
            "message": "Por favor, defina um nome para a busca."
        }), 400
            
    prompt_solicitacao = f"""
    Compile um dossiê completo, aprofundado e minucioso de caráter histórico-forense para o alvo: {pesquisa}.
    Certifique-se de expor de forma detalhada o percurso criminal, o julgamento, a execução ou andamento de penas e o estado de custódia do indivíduo.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_solicitacao,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=DOSSIE_SCHEMA,
                temperature=0.15
            )
        )
        
        dossie_dados = json.loads(response.text)
        
        return jsonify({
            "status": "success",
            "dados": dossie_dados
        }), 200
        
    except APIError as e:
        return jsonify({
            "status": "error",
            "message": f"Erro de comunicação de banco de dados (API Gemini): {e.message}"
        }), 503
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Instabilidade no processamento interno do dossiê: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)