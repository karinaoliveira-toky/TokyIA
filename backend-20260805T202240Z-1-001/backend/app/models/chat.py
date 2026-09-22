from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    mensagem: str

class FonteDocumento(BaseModel):
    titulo: str
    tipo: str
    url_simulada: str
    relevancia: float
    conteudo: Optional[str] = None

class ChatResponse(BaseModel):
    resposta: str
    fontes: List[FonteDocumento]
    modo: str
    bloqueado: bool = False

class LogRequest(BaseModel):
    mensagem_id: str
    prompt_usuario: str
    resposta_ia: str
    feedback: Optional[str] = None
