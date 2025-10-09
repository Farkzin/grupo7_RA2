from abc import ABC, abstractmethod

class CacheInterface(ABC):
    """Interface base para algoritmos de cache."""

    @abstractmethod
    def get_text(self, text_id: int) -> str:
        """Retorna o texto, consultando o cache ou o disco."""
        pass
