import random
import numpy as np
import matplotlib.pyplot as plt
from algorithms.fifo_cache import FIFOCache
from algorithms.lru_cache import LRUCache
from algorithms.lfu_cache import LFUCache

class CacheSimulator:
    def __init__(self):
        self.algorithms = {
            "FIFO": FIFOCache(),
            "LRU": LRUCache(),
            "LFU": LFUCache()
        }


    def run_user_simulation(self, cache, mode: str, n_requests=200):
        results = []
        for _ in range(n_requests):
            if mode == "aleatorio":
                text_id = random.randint(1, 100)
            elif mode == "poisson":
                text_id = min(max(int(np.random.poisson(40)), 1), 100)
            elif mode == "ponderado":
                if random.random() < 0.43:
                    text_id = random.randint(30, 40)
                else:
                    text_id = random.randint(1, 100)
            else:
                continue

            content = cache.get_text(text_id)
            stats = cache.stats
            results.append((stats.hits, stats.misses, stats.last_time))

        return results

    def run_all(self):
        for name, cache in self.algorithms.items():
            print(f"\n--- Simulando {name} ---")
            for mode in ["aleatorio", "poisson", "ponderado"]:
                res = self.run_user_simulation(cache, mode)
                print(f"{name} ({mode}) finalizado.")

        print("\nSimulação concluída.")

if __name__ == "__main__":
    sim = CacheSimulator()
    sim.run_all()
