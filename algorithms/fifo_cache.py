from algorithms.cache_base import CacheBase

class FIFOCache(CacheBase):

    """FIFO: remove o item mais antigo quando lotar (10)."""

    def __init__(self):
        super().__init__()  # construtor de CacheBase
        self.order = []     # vetor de IDs na ordem de inserção

    def _on_hit(self, text_id: int) -> None:
        # FIFO não muda ordem em hits
        return

    def _insert(self, text_id: int, content: str) -> None:
        # cheio: remove o mais antigo 
        if len(self.storage) >= self.capacity:
            oldest_id = self.order.pop(0)
            self.storage.pop(oldest_id, None)
               
        # insere novo
        self.storage[text_id] = content
        self.order.append(text_id)