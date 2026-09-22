import asyncio
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse, LogRequest
from app.core.config import settings
from app.core.security import (
    verificar_tema_proibido, 
    verificar_fora_de_escopo, 
    verificar_concorrente_externo,
    RESPOSTA_BLOQUEIO
)
from app.services.databricks_sql_service import DatabricksSQLService
from app.services.ai_service import AIService
from app.models.chat import FonteDocumento

router = APIRouter()

@router.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "TokyIA API está online. Use /docs para a documentação Swagger UI."}

@router.get("/status", tags=["Health Check"])
async def status():
    return {
        "sistema": settings.PROJECT_NAME,
        "versao": settings.PROJECT_VERSION,
        "status": "online",
        "modo": "producao",
        "provedor_rag": settings.RETRIEVAL_PROVIDER,
    }

@router.post("/chat", response_model=ChatResponse, tags=["Inteligência Estratégica"])
async def chat(request: ChatRequest):
    try:
        msg = request.mensagem.strip()

        # 1. Filtro Zero Tolerância
        if verificar_tema_proibido(msg):
            return ChatResponse(
                resposta=RESPOSTA_BLOQUEIO,
                fontes=[],
                modo="producao",
                bloqueado=True
            )

        # 2. Fora de Escopo
        desvio = verificar_fora_de_escopo(msg)
        if desvio:
            return ChatResponse(
                resposta=desvio,
                fontes=[],
                modo="producao",
                bloqueado=False
            )

        # 3. Concorrentes
        aviso_concorrente = verificar_concorrente_externo(msg)
        if aviso_concorrente:
            return ChatResponse(
                resposta=aviso_concorrente,
                fontes=[],
                modo="producao",
                bloqueado=False
            )

        # 4. Text-to-SQL Pipeline
        # 4.1. Gerar query SQL a partir do prompt
        sql_query = AIService.gerar_sql(msg)
        
        if sql_query.startswith("ERRO_COLUNA_INEXISTENTE:"):
            colunas_disponiveis = sql_query.replace("ERRO_COLUNA_INEXISTENTE:", "").strip()
            resposta_erro = f"⚠️ Não encontrei a coluna solicitada no dicionário da tabela. Por favor, utilize uma das colunas disponíveis: {colunas_disponiveis}"
            return ChatResponse(
                resposta=resposta_erro,
                fontes=[],
                modo="producao"
            )

        # 4.2. Executar query no Databricks SQL Warehouse
        try:
            resultados = DatabricksSQLService.executar_query(sql_query)
            executada_com_sucesso = True
            erro_msg = None
        except Exception as e:
            resultados = []
            executada_com_sucesso = False
            erro_msg = str(e)
            
        # 4.3. Gerar resposta final combinando a pergunta e os dados retornados
        resposta = AIService.gerar_resposta_final(msg, sql_query, resultados)
        if not executada_com_sucesso:
            resposta = f"{resposta}\n\n*⚠️ Erro ao executar a consulta no Databricks: {erro_msg}*"

        # Formata a consulta SQL como uma "FonteDocumento" auditável
        fonte_sql = FonteDocumento(
            titulo="Consulta SQL Databricks",
            tipo="SQL",
            url_simulada="#",
            relevancia=1.0,
            conteudo=sql_query
        )
        
        return ChatResponse(
            resposta=resposta,
            fontes=[fonte_sql],
            modo="producao"
        )

    except Exception as e:
        print(f"[ERRO] {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor TokyIA.")

@router.post("/logs", tags=["Auditoria & Feedback"])
async def registrar_log(request: LogRequest):
    try:
        # Mock de persistência de logs e feedbacks
        # TODO: Assim que a TI fornecer a DATABASE_URL, substituir o bloco abaixo pelo INSERT real:
        # db.execute("INSERT INTO chat_logs (mensagem_id, prompt_usuario, resposta_ia, feedback) VALUES (...)"
        
        print("\n" + "="*80)
        print("📥 [REGISTRO DE LOG / FEEDBACK DE DIRETORIA]")
        print(f"🆔 ID da Mensagem: {request.mensagem_id}")
        print(f"💬 Prompt do Usuário: {request.prompt_usuario}")
        print(f"🤖 Resposta da TokyIA:\n{request.resposta_ia}")
        print(f"⭐ Avaliação do Diretor: {'👍 ÚTIL' if request.feedback == 'positivo' else '👎 NÃO ÚTIL' if request.feedback == 'negativo' else 'Sem avaliação'}")
        print("="*80 + "\n")
        
        return {"status": "sucesso", "mensagem": "Log e feedback registrados com sucesso!"}
        
    except Exception as e:
        print(f"[ERRO LOG] Falha ao registrar log: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao registrar log.")
