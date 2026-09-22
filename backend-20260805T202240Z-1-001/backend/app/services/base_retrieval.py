from abc import ABC, abstractmethod
from typing import List
from app.models.chat import FonteDocumento

class BaseRetrievalService(ABC):
    @abstractmethod
    def buscar_fontes(self, mensagem: str, top_k: int = 3) -> List[FonteDocumento]:
        """
        Realiza a busca de fontes relevantes com base na mensagem de entrada.
        """
        pass
