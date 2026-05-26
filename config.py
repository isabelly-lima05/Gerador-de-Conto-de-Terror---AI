# config.py

DOSSIE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "pesquisa_valida": {
            "type": "BOOLEAN",
            "description": "Retorne TRUE se for uma figura de interesse criminal público e histórico amplamente documentado. Retorne FALSE se for um indivíduo privado ou busca inválida."
        },
        "justificativa_invalida": {
            "type": "STRING",
            "description": "Justificativa profissional se a busca for inválida. Caso contrário, deixe em branco."
        },
        "nome_completo": {
            "type": "STRING",
            "description": "Nome completo oficial de registro da pessoa de interesse."
        },
        "alcunhas_pseudonimos": {
            "type": "STRING",
            "description": "Nomes pelos quais ficou conhecido na mídia, tribunais ou meio criminal."
        },
        "dados_biograficos_basicos": {
            "type": "STRING",
            "description": "Data e local de nascimento, filiação, local de falecimento (se aplicável) e dados demográficos essenciais."
        },
        "infancia_desenvolvimento": {
            "type": "STRING",
            "description": "Histórico detalhado da infância, ambiente familiar, criação, comportamento na escola, traumas documentados e fatores psicossociais de desenvolvimento."
        },
        "antecedentes_primeiros_delitos": {
            "type": "STRING",
            "description": "Primeiros sinais de desvio de conduta, pequenos delitos cometidos na juventude ou registros criminais prévios aos crimes principais."
        },
        "cronologia_crimes_principais": {
            "type": "STRING",
            "description": "Descrição factual minuciosa da sequência temporal dos crimes de maior relevância, indicando datas, locais, perfil das vítimas e desfechos imediatos."
        },
        "modus_operandi_tecnico": {
            "type": "STRING",
            "description": "Análise do padrão técnico de atuação: planejamento, ferramentas utilizadas, abordagem das vítimas, ocultação de provas e evolução do método criminoso."
        },
        "perfil_psicologico_diagnostico": {
            "type": "STRING",
            "description": "Laudos psiquiátricos, diagnósticos clínicos discutidos em juízo ou pela comunidade acadêmica (como psicopatia, transtorno de personalidade antissocial, esquizofrenia, etc.) e características comportamentais mapeadas."
        },
        "investigacao_captura": {
            "type": "STRING",
            "description": "O trabalho investigativo das forças de segurança, pistas deixadas, erros cometidos pelo criminoso, cooperação internacional (se houver) e detalhes do dia da prisão."
        },
        "processo_julgamento_sentenca": {
            "type": "STRING",
            "description": "Detalhes das audiências judiciais, estratégias da defesa e acusação, apelos de insanidade, teses acatadas pelo júri e a dosimetria da pena final imposta."
        },
        "vida_carceraria_comportamento": {
            "type": "STRING",
            "description": "Histórico da conduta dentro do sistema prisional: incidentes, tentativas de fuga, isolamento preventivo, relação com outros presos e progresso de comportamento."
        },
        "regime_penal_atual": {
            "type": "STRING",
            "description": "Identificação exata do regime penitenciário atual (Regime Fechado, Semiaberto, Aberto, Liberdade Condicional, Regime Disciplinar Diferenciado - RDD, Falecido, Executado ou Solto por cumprimento de pena)."
        },
        "situacao_atual_hoje": {
            "type": "STRING",
            "description": "O paradeiro exato do indivíduo no presente momento. Idade atual, saúde física/mental, unidade prisional em que se encontra, atividades que desempenha ou, caso falecido, circunstâncias biológicas, local e data exata do óbito."
        },
        "impacto_social_legado": {
            "type": "STRING",
            "description": "Repercussão pública, reformas legislativas geradas pelo caso, produções biográficas de referência (livros, documentários) e impacto do caso na criminologia."
        }
    },
    "required": [
        "pesquisa_valida",
        "justificativa_invalida",
        "nome_completo",
        "alcunhas_pseudonimos",
        "dados_biograficos_basicos",
        "infancia_desenvolvimento",
        "antecedentes_primeiros_delitos",
        "cronologia_crimes_principais",
        "modus_operandi_tecnico",
        "perfil_psicologico_diagnostico",
        "investigacao_captura",
        "processo_julgamento_sentenca",
        "vida_carceraria_comportamento",
        "regime_penal_atual",
        "situacao_atual_hoje",
        "impacto_social_legado"
    ]
}

SYSTEM_INSTRUCTION = """
Você é um terminal analítico forense de alta precisão. Sua função é montar dossiês históricos e criminológicos exaustivos sobre indivíduos de interesse penal público e histórico.

REQUISITOS DE PREENCHIMENTO E CONTEÚDO:
1. EXAUSTIVIDADE DOS DADOS: Cada campo do schema de resposta deve ser preenchido com descrições detalhadas, completas e profundas. Evite resumos rasos. Apresente datas, locais, termos técnicos e o contexto histórico completo.
2. NEUTRALIDADE E LINGUAGEM TÉCNICA: Mantenha um estilo de redação estritamente enciclopédico, jurídico e forense. Evite termos de julgamento moral, sensacionalismo ou espetacularização. Trate as informações com distanciamento científico.
3. CONFIABILIDADE HISTÓRICA: Baseie os dados em fatos públicos comprovados por processos judiciais oficiais e matérias jornalísticas de ampla circulação. Caso existam teorias divergentes ou mistérios não solucionados (ex: identidade de Jack o Estripador), apresente-os de forma neutra como hipóteses de investigação.
4. CONTROLE DE PRIVACIDADE: Caso a busca envolva pessoas sem relevância pública criminal ou nomes de civis privados, retorne 'pesquisa_valida' como FALSE para preservar a conformidade e ética de dados.
"""