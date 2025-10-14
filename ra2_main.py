

from core.text_manager import TextManager
from algorithms.lru_cache import LRUCache
from algorithms.fifo_cache import FIFOCache
from algorithms.lfu_cache import LFUCache
from algorithms.mru_cache import MRUCache
from simulation.simulator import CacheSimulator

def choose_cache():

    """Menu. Retorna uma instância do cache escolhido."""

    print("Escolha o algoritmo: (1) FIFO (2) LRU (3) LFU (4) MRU.")
    while True:
        choice = input("> ").strip()
        match choice:
            case "1":
                return FIFOCache()  # política FIFO
            case "2":
                return LRUCache()  # política LRU
            case "3":
                return LFUCache()  # política LFU
            case "4":
                return MRUCache()  # política MRU
            case _:
                # trata entradas erradas
                print("Opção inválida. Digite 1, 2, 3 ou 4.")

def main():

    """Loop principal. Lê comandos do usuário e executa ação."""

    print("===== Leitor de Textos - Projeto RA2 =====")
    cache = choose_cache() # ponto-chave: instância única do cache na sessão

    while True:
        try:
            text_id = int(input("Digite o número do texto (1 a 100), 0 sair, -1 simulação: "))
            # Encerra o programa
            if text_id == 0:
                print("Encerrando o programa...")
                break
            # Entra em modo simulação
            elif text_id == -1:
                print("Entrando no modo simulação...\n")
                sim = CacheSimulator()
                sim.run_all()
                continue
            # Chama o arquivo .txt respectivo ao número digitado e armazena em cache
            elif 1 <= text_id <= 100:
                content = cache.get_text(text_id)
                print(f"\n--- Texto {text_id} ---\n")
                print(content[:500] + "...\n")
                print("--------------------------\n")
                print(f"Requests: {cache.stats.requests} | Hits: {cache.stats.hits} | Misses: {cache.stats.misses} | Tempo da última requisição: {cache.stats.last_time:.4f}s | Tempo total: {cache.stats.total_time:.4f}s\n")
            else:
                # Trata entradas erradas
                print("Número inválido.")
                # Trata entradas erradas
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

if __name__ == "__main__":
    main()
