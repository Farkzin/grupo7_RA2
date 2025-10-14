# mru_cache.py
# Implementa��o do algoritmo de substitui��o de cache MRU (Most Recently Used)


from algorithms.cache_base import CacheBase

class MRUCache(CacheBase):
    """MRU: remove o item mais recentemente usado (oposto do LRU)."""

    def __init__(self):
        super().__init__()
        self.order = []  # mant�m a ordem de uso (mais recente no fim)

    def _on_hit(self, text_id: int) -> None:
        """
        Quando um item � acessado (hit), ele se torna o mais recentemente usado.
        Portanto, movemos o ID dele para o final da lista.
        """
        if text_id in self.order:
            self.order.remove(text_id)
            self.order.append(text_id)

    def _insert(self, text_id: int, content: str) -> None:
        """
        Insere novo item no cache.
        Se estiver cheio, remove o MAIS recentemente usado (�ltimo da lista).
        """
        if text_id in self.order:
            self.order.remove(text_id)

        # Se o cache estiver cheio, remove o item mais recentemente usado
        if len(self.storage) >= self.capacity:
            mru_id = self.order.pop(-1)  # remove o �ltimo (mais recente)
            self.storage.pop(mru_id, None)

        # Adiciona o novo item no final (agora � o mais recente)
        self.storage[text_id] = content
        self.order.append(text_id)
