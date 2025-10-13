from algorithms.cache_base import CacheBase

class LFUCache(CacheBase):
    """LFU: remove o item menos frequentemente usado."""

    def __init__(self):
        super().__init__()
        self.freq = {}  # id -> frequência de acessos

    def _on_hit(self, text_id: int) -> None:
        # Incrementa a frequência quando o item é acessado
        self.freq[text_id] = self.freq.get(text_id, 0) + 1


    def _insert(self, text_id: int, content: str) -> None:
        # Se o cache estiver cheio, remove o item menos usado
        if len(self.storage) >= self.capacity:
            # selecionar apenas entre chaves que existem em freq; fallback para storage keys
            candidates = {k: self.freq.get(k, 0) for k in self.storage.keys()}
            lfu_id = min(candidates, key=candidates.get)
            self.storage.pop(lfu_id, None)
            self.freq.pop(lfu_id, None)

        # Insere o novo item
        self.storage[text_id] = content
        self.freq[text_id] = self.freq.get(text_id, 0) + 1


        # Insere o novo item
        self.storage[text_id] = content
        self.freq[text_id] = 1
    