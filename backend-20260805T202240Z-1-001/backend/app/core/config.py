import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "TokyIA Backend"
    PROJECT_VERSION: str = "3.1.0"
    
    # Provedor de Busca (exclusivamente databricks_sql)
    RETRIEVAL_PROVIDER: str = "databricks_sql"
    
    # Configurações de API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABRICKS_HOST: str = os.getenv("DATABRICKS_HOST", "")
    DATABRICKS_TOKEN: str = os.getenv("DATABRICKS_TOKEN", "")
    DATABRICKS_SQL_HTTP_PATH: str = os.getenv("DATABRICKS_SQL_HTTP_PATH", "")

settings = Settings()
