import random, csv, os, time
import numpy as np
import matplotlib.pyplot as plt
import time

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
            r = random.randint(1, 89)          # exclui 30–40 do restante
            return r if r < 30 else r + 11
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
        import os, glob
        import pandas as pd
        import matplotlib.pyplot as plt

        files = glob.glob(os.path.join(OUTPUT_DIR, "*.csv"))
        if not files:
            print("Sem CSVs."); return

        df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
        df = df.sort_values(["algo", "mode", "user", "req_id"])

        # garantir colunas
        if "hit" not in df.columns:
            df["hits"] = pd.to_numeric(df.get("hits", 0), errors="coerce").fillna(0).astype(int)
            df["hit"] = (df.groupby(["algo","mode","user"])["hits"]
                        .diff().fillna(df["hits"]).clip(0,1).astype(int))
        if "latency_ms" not in df.columns:
            df["latency_ms"] = pd.to_numeric(df.get("last_time", 0), errors="coerce") * 1000
        df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
        df = df.dropna(subset=["latency_ms"])
        if df.empty:
            print("Sem dados válidos."); return

        # 1) Latência média por algoritmo
        m1 = df.groupby("algo")["latency_ms"].mean().sort_values()
        ax = m1.plot(kind="bar", title="Latência média por algoritmo")
        ax.set_ylabel("ms"); fig = ax.get_figure(); fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "latency_mean_by_algo.png")); plt.close(fig)

        # 2) Latência média por algoritmo e tipo (hit/miss)
        m2 = (df.groupby(["algo","hit"])["latency_ms"].mean()
                .unstack("hit").rename(columns={0:"miss",1:"hit"}).fillna(0))
        ax = m2.plot(kind="bar", title="Latência média por algoritmo e tipo")
        ax.set_ylabel("ms"); fig = ax.get_figure(); fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "latency_mean_by_algo_hit.png")); plt.close(fig)

        # 3) Hit rate (%) por algoritmo
        hr_algo = df.groupby("algo")["hit"].mean().mul(100).sort_values()
        ax = hr_algo.plot(kind="bar", title="Hit rate (%) por algoritmo")
        ax.set_ylabel("%"); fig = ax.get_figure(); fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "hit_rate_by_algo.png")); plt.close(fig)

        # 4) Hit rate (%) por algoritmo e modo
        hr_am = (df.groupby(["algo","mode"])["hit"].mean().mul(100)
                .unstack("mode").fillna(0))
        ax = hr_am.plot(kind="bar", title="Hit rate (%) por algoritmo e modo")
        ax.set_ylabel("%"); fig = ax.get_figure(); fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "hit_rate_by_algo_mode.png")); plt.close(fig)

        # 5) Latência p95 por algoritmo (ms)
        p95 = df.groupby("algo")["latency_ms"].quantile(0.95).sort_values()
        ax = p95.plot(kind="bar", title="Latência p95 por algoritmo")
        ax.set_ylabel("ms"); fig = ax.get_figure(); fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "latency_p95_by_algo.png")); plt.close(fig)

        # 6) Top 20 textos por taxa de miss (%)
        miss_rate = (1 - df.groupby("text_id")["hit"].mean()).mul(100)
        top_miss = miss_rate.sort_values(ascending=False).head(20)
        ax = top_miss.plot(kind="bar", title="Top 20 textos por taxa de miss")
        ax.set_ylabel("%"); fig = ax.get_figure(); fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "top20_miss_texts.png")); plt.close(fig)

        print("Gráficos salvos em", OUTPUT_DIR)

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