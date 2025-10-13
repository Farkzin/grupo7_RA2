from core.text_manager import TextManager
from simulation.simulator import CacheSimulator

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def main():
    print("===== Leitor de Textos - Projeto RA2 =====")
    print("Digite o número do texto (1 a 100):")
    print("0 - Sair | -1 - Modo Simulação\n")

    while True:
        try:
            text_id = int(input("> "))

            if text_id == 0:
                print("Encerrando o programa...")
                break
            elif text_id == -1:
                print("Entrando no modo simulação...\n")
                sim = CacheSimulator()
                sim.run_all()
                print("\nSimulação concluída! Retornando ao menu principal...\n")
                continue
            elif 1 <= text_id <= 100:
                text = TextManager.load_text(text_id)
                print(f"\n--- Texto {text_id} ---\n")
                print(text[:500] + "...\n")
                print("--------------------------\n")
            else:
                print("Número inválido. Digite entre 1 e 100, ou 0/-1.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

if __name__ == "__main__":
    main()
