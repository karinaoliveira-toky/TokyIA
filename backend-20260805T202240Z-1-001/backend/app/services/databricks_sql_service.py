import re
from typing import List, Dict, Any
from databricks import sql
from app.core.config import settings

class DatabricksSQLService:
    """
    Serviço oficial de conexão e execução de queries SQL no Databricks SQL Warehouse.
    """
    
    @staticmethod
    def validar_query_segura(query: str) -> bool:
        """
        Verifica se a consulta é estritamente de leitura (SELECT, WITH, SHOW, DESCRIBE).
        Retorna False se contiver palavras-chave de alteração ou manipulação de dados.
        """
        # Limpa espaços e converte para minúsculas
        query_clean = query.strip().lower()
        
        # Palavras-chave proibidas
        palavras_proibidas = [
            r"\binsert\b", r"\bupdate\b", r"\bdelete\b", 
            r"\bdrop\b", r"\balter\b", r"\bcreate\b", 
            r"\bgrant\b", r"\brevoke\b", r"\btruncate\b", 
            r"\bmerge\b", r"\breplace\b"
        ]
        
        for palavra in palavras_proibidas:
            if re.search(palavra, query_clean):
                return False
        
        # Deve começar com SELECT, WITH, SHOW ou DESCRIBE
        if not (query_clean.startswith("select") or query_clean.startswith("with") or query_clean.startswith("show") or query_clean.startswith("describe") or query_clean.startswith("desc")):
            return False
            
        return True

    @staticmethod
    def formatar_limite_query(query: str) -> str:
        """
        Garante que a query SELECT/WITH tenha um limite máximo de 100 resultados para evitar sobrecargas.
        """
        query_strip = query.strip()
        if query_strip.endswith(";"):
            query_strip = query_strip[:-1].strip()
            
        query_lower = query_strip.lower()
        # Se for SELECT ou WITH e não tiver LIMIT, adicionamos um LIMIT 100
        if (query_lower.startswith("select") or query_lower.startswith("with")) and not re.search(r"\blimit\s+\d+", query_lower):
            query_strip = f"{query_strip} LIMIT 100"
            
        return query_strip

    @classmethod
    def executar_query(cls, sql_query: str) -> List[Dict[str, Any]]:
        """
        Conecta ao SQL Warehouse e executa a query SQL retornando uma lista de dicionários.
        """
        if not settings.DATABRICKS_HOST or not settings.DATABRICKS_TOKEN or not settings.DATABRICKS_SQL_HTTP_PATH:
            raise ValueError("Configurações do Databricks SQL Warehouse incompletas no ambiente.")

        # 1. Validação de Segurança
        if not cls.validar_query_segura(sql_query):
            raise PermissionError("Apenas consultas de leitura (SELECT) são permitidas por motivos de segurança.")

        # 2. Formatação do Limite
        sql_query = cls.formatar_limite_query(sql_query)

        print(f"[DATABRICKS SQL] Executando query: {sql_query}")
        
        try:
            connection = sql.connect(
                server_hostname=settings.DATABRICKS_HOST.replace("https://", "").replace("/", ""),
                http_path=settings.DATABRICKS_SQL_HTTP_PATH,
                access_token=settings.DATABRICKS_TOKEN
            )
            
            cursor = connection.cursor()
            cursor.execute(sql_query)
            
            # Recupera as colunas do cursor
            colunas = [col[0] for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            
            resultados = []
            for row in rows:
                resultados.append(dict(zip(colunas, row)))
                
            cursor.close()
            connection.close()
            
            print(f"[DATABRICKS SQL] Executado com sucesso. {len(resultados)} registros retornados.")
            return resultados
            
        except Exception as e:
            print(f"[ERRO DATABRICKS SQL]: {str(e)}")
            raise e
