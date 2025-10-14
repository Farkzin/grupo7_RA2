# mru_cache.py
# Implementação do algoritmo de substituição de cache MRU (Most Recently Used)


from algorithms.cache_base import CacheBase

class MRUCache(CacheBase):
    """MRU: remove o item mais recentemente usado (oposto do LRU)."""

    def __init__(self):
        super().__init__()
        self.order = []  # mantém a ordem de uso (mais recente no fim)

    def _on_hit(self, text_id: int) -> None:
        """
        Quando um item é acessado (hit), ele se torna o mais recentemente usado.
        Portanto, movemos o ID dele para o final da lista.
        """
        if text_id in self.order:
            self.order.remove(text_id)
            self.order.append(text_id)

    def _insert(self, text_id: int, content: str) -> None:
        """
        Insere novo item no cache.
        Se estiver cheio, remove o MAIS recentemente usado (último da lista).
        """
        if text_id in self.order:
            self.order.remove(text_id)

        # Se o cache estiver cheio, remove o item mais recentemente usado
        if len(self.storage) >= self.capacity:
            mru_id = self.order.pop(-1)  # remove o último (mais recente)
            self.storage.pop(mru_id, None)

        # Adiciona o novo item no final (agora é o mais recente)
        self.storage[text_id] = content
        self.order.append(text_id)
