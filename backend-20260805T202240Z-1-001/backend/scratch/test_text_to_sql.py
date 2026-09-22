import os
import sys

# Garante que o diretório raiz do backend esteja no sys.path para podermos importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.core.config import settings
from app.services.ai_service import AIService
from app.services.databricks_sql_service import DatabricksSQLService

def test_pipeline():
    pergunta = "Qual foi o GMV total de vendas no canal Loja Física no primeiro trimestre de 2026?"
    print(f"Diretor: '{pergunta}'\n")
    
    # 1. Gerar query SQL
    print("1. Gerando query SQL no Gemini...")
    sql_query = AIService.gerar_sql(pergunta)
    print(f"Query SQL Gerada:\n{sql_query}\n")
    
    # 2. Executar no Databricks
    print("2. Executando query no Databricks SQL Warehouse...")
    try:
        resultados = DatabricksSQLService.executar_query(sql_query)
        print(f"Número de registros retornados: {len(resultados)}")
        if resultados:
            print(f"Exemplo de linha: {resultados[0]}\n")
    except Exception as e:
        print(f"Erro ao executar query: {e}")
        resultados = []
        
    # 3. Gerar resposta final
    print("3. Formulando resposta executiva no Gemini...")
    resposta = AIService.gerar_resposta_final(pergunta, sql_query, resultados)
    print(f"Resposta Final TokyIA:\n{resposta}\n")

if __name__ == "__main__":
    test_pipeline()
