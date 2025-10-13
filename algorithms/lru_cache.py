from algorithms.cache_base import CacheBase

class LRUCache(CacheBase):
    """LRU: remove o item menos recentemente usado."""

    def __init__(self):
        super().__init__()
        self.order = []  # mantém a ordem de uso (mais recente no fim)

    def _on_hit(self, text_id: int) -> None:
        # move o item acessado para o final (mais recentemente usado)
        if text_id in self.order:
            self.order.remove(text_id)
            self.order.append(text_id)

    def _insert(self, text_id: int, content: str) -> None:
        # se estiver cheio, remove o menos recentemente usado (primeiro da lista)
        if len(self.storage) >= self.capacity:
            lru_id = self.order.pop(0)
            self.storage.pop(lru_id, None)

        # adiciona o novo item no final da lista
        self.storage[text_id] = content
        if text_id in self.order:
            self.order.remove(text_id)
        self.order.append(text_id)
