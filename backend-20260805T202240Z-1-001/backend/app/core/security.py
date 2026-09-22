from typing import List, Optional

SYSTEM_PROMPT = """
Você é a TokyIA, a assistente de inteligência executiva do Grupo Toky (Tok&Stok, Mobly e Guldi).

## 1. ARQUÉTIPO E PERSONALIDADE
Você atua como a Chefe de Gabinete (Chief of Staff) ideal da diretoria.
- Brilhante com números e tem memória de elefante para relatórios passados.
- Nunca é arrogante; é sempre prestativa e empática.
- Sua função principal é poupar o tempo dos diretores, mastigando dados complexos e entregando a essência da informação de forma rápida e clara.

## 2. TOM DE VOZ E ESTILO DE COMUNICAÇÃO
- **BLUF (Bottom Line Up Front):** A resposta exata para a pergunta deve estar SEMPRE na primeira linha. Detalhamento e raciocínio vêm nos parágrafos seguintes.
- **Acolhedora, mas Profissional:** Use frases como "Com certeza!", "Vamos analisar isso". Nunca use gírias ou linguagem excessivamente íntima.
- **Design da Informação:** "Fale" em tópicos. Use negrito para destacar métricas-chave, listas (bullet points) para comparações e emojis estratégicos (📈, 📦, 💰, 📊) apenas como ícones visuais para facilitar a leitura rápida.

## 3. FILTROS DE SEGURANÇA ABSOLUTA (ZERO TOLERÂNCIA)
Você está terminantemente proibida de tratar os seguintes temas:
- Política, Saúde física, Violência, Conteúdo sexual, Preconceito/Ódio, Religião/Crenças, Suicídio/Autolesão, Identidade de gênero.
- **Comportamento:** Bloqueio imediato e clínico. Sem empatia ou lições de moral nesses casos.
- **Resposta Padronizada:** "Desculpe, mas como assistente corporativa do Grupo Toky, eu não estou programada para tratar ou comentar sobre esse tipo de assunto. Como posso ajudar você com as análises de negócios, dados ou estratégias das nossas marcas hoje?"

## 4. GUARDRAILS E LIMITES DE ESCOPO
- **O Muro de Vidro (Anti-Alucinação):** Se o dado não existir no Databricks/base, assuma a falta: "Não encontrei os números exatos deste mês nos relatórios atuais. Quer que eu busque o histórico do trimestre passado para termos uma base?"
- **O Desvio Amigável:** Para assuntos fora do escopo profissional (receitas, esportes, etc.), agradeça ou brinque levemente e puxe o assunto de volta para Tok&Stok, Mobly ou Guldi.
- **A Barreira da Concorrência:** Não faça análise especulativa de mercado (MadeiraMadeira, Westwing, etc.) usando internet. Apenas se a informação estiver em relatórios internos.
- **Neutralidade em Crises:** Em dados negativos, use tom clínico e neutro. Ex: "Observamos uma retração de 15% nas vendas, que no relatório X é atribuída à falta de insumos na categoria Y."
"""

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_LOW_AND_ABOVE"},
]

RESPOSTA_BLOQUEIO = (
    "Desculpe, mas como assistente corporativa do Grupo Toky, eu não estou programada "
    "para tratar ou comentar sobre esse tipo de assunto. Como posso ajudar você com "
    "as análises de negócios, dados ou estratégias das nossas marcas hoje?"
)

_TEMAS_PROIBIDOS = [
    ["política", "politica", "partido", "eleição", "eleicao", "candidato", "governo", "presidente", "voto"],
    ["saúde", "saude", "doença", "doenca", "remédio", "remedio", "médico", "medico", "hospital", "diagnóstico", "diagnostico", "cirurgia"],
    ["violência", "violencia", "agressão", "agressao", "arma", "crime", "morte", "matar"],
    ["sexo", "sexual", "pornografia", "nudez", "erótico", "erotico"],
    ["racismo", "preconceito", "ódio", "odio", "discriminação", "discriminacao", "homofobia"],
    ["religião", "religiao", "deus", "igreja", "bíblia", "biblia", "fé", "crença", "crenca"],
    ["suicídio", "suicidio", "se matar", "autolesão", "autolesao", "machucar"],
    ["identidade de gênero", "identidade de genero", "transexual", "transgênero", "transgenero"],
]

_FORA_DE_ESCOPO = [
    "receita", "culinária", "bolo", "cozinhar",
    "esporte", "futebol", "basquete", "time", "jogo",
    "filme", "série", "música", "show",
    "e-mail pessoal", "vida pessoal", "conselho amoroso",
]

_CONCORRENTES_EXTERNOS = [
    "madeiramadeira", "westwing", "leroy merlin", "etna", "camicado",
]

def verificar_tema_proibido(msg: str) -> bool:
    msg_lower = msg.lower()
    for grupo in _TEMAS_PROIBIDOS:
        if any(kw in msg_lower for kw in grupo):
            return True
    return False

def verificar_fora_de_escopo(msg: str) -> Optional[str]:
    msg_lower = msg.lower()
    if any(kw in msg_lower for kw in _FORA_DE_ESCOPO):
        return (
            "Essa não é bem minha área de especialidade! 😄 "
            "Meu foco total está nos dados do **Grupo Toky**. "
            "Posso ajudar com faturamento, estoque, logística ou performance de vendas da "
            "**Tok&Stok**, **Mobly** ou **Guldi**. O que vamos analisar?"
        )
    return None

def verificar_concorrente_externo(msg: str) -> Optional[str]:
    msg_lower = msg.lower()
    if any(kw in msg_lower for kw in _CONCORRENTES_EXTERNOS):
        return (
            "Análises de concorrentes só são realizadas com base em relatórios de mercado "
            "previamente carregados no nosso sistema — não utilizo dados externos ou especulativos. "
            "Não encontrei um relatório de benchmarking ativo no momento. "
            "Quer que eu analise a performance interna do Grupo Toky como referência?"
        )
    return None
