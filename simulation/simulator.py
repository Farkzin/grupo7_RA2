import random, csv, os, time
import numpy as np
import matplotlib.pyplot as plt

from algorithms.fifo_cache import FIFOCache
from algorithms.lru_cache import LRUCache
from algorithms.lfu_cache import LFUCache

OUTPUT_DIR = "simulation_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALGO_CLASSES = {
    "FIFO": FIFOCache,
    "LRU": LRUCache,
    "LFU": LFUCache
}

MODES = ["aleatorio", "poisson", "ponderado"]
REQUESTS_PER_USER = 200
USERS = 3

class CacheSimulator:
    def __init__(self):
        pass

    def _gen_request(self, mode):
        if mode == "aleatorio":
            return random.randint(1, 100)
        elif mode == "poisson":
            return min(max(int(np.random.poisson(40)), 1), 100)
        elif mode == "ponderado":
            if random.random() < 0.43:
                return random.randint(30, 40)
            else:
                # distribuir uniformemente exceto intervalo preferido
                r = random.randint(1, 100)
                return r
        else:
            raise ValueError("Modo desconhecido")

    def run_user(self, algo_name, algo_class, mode, user_id):
        cache = algo_class()  # nova instância por usuário
        results = []
        for req_id in range(1, REQUESTS_PER_USER + 1):
            tid = self._gen_request(mode)
            start = time.perf_counter()
            _ = cache.get_text(tid)
            duration = cache.stats.last_time  # CacheBase já mede e guarda last_time
            # coletar snapshot dos counters para esta requisicao
            results.append({
                "algo": algo_name,
                "user": user_id,
                "mode": mode,
                "req_id": req_id,
                "text_id": tid,
                "requests": cache.stats.requests,
                "hits": cache.stats.hits,
                "misses": cache.stats.misses,
                "last_time": duration
            })
        # salvar CSV por usuário
        fname = os.path.join(OUTPUT_DIR, f"{algo_name}_{mode}_user{user_id}.csv")
        keys = results[0].keys()
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        return results

    def aggregate_and_plot(self):
        # Exemplo rápido: calcular hit rate médio por algoritmo e modo
        import glob, pandas as pd
        all_files = glob.glob(os.path.join(OUTPUT_DIR, "*.csv"))
        df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
        summary = df.groupby(["algo", "mode", "user"]).agg({
            "hits": "max",
            "misses": "max",
            "last_time": "mean"
        }).reset_index()
        # hit rate
        summary["hit_rate"] = summary["hits"] / (summary["hits"] + summary["misses"])
        # plot hit rate por algoritmo (média entre users e modos)
        plot = summary.groupby("algo")["hit_rate"].mean().sort_values()
        ax = plot.plot(kind="bar", title="Hit rate médio por algoritmo")
        fig = ax.get_figure()
        fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "hit_rate_mean_by_algo.png"))
        print("Gráfico salvo em", os.path.join(OUTPUT_DIR, "hit_rate_mean_by_algo.png"))

    def run_all(self):
        for algo_name, algo_class in ALGO_CLASSES.items():
            for mode in MODES:
                for user in range(1, USERS + 1):
                    print(f"Executando {algo_name} | {mode} | user{user}")
                    self.run_user(algo_name, algo_class, mode, user)
        print("Todas as simulações concluídas. Agregando resultados...")
        self.aggregate_and_plot()

if __name__ == "__main__":
    sim = CacheSimulator()
    sim.run_all()
