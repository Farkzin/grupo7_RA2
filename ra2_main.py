from core.text_manager import TextManager

# (posteriormente você importará o cache, ex: from algorithms.fifo_cache import FIFOCache)
# cache = FIFOCache()

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
                print("Entrando no modo simulação...")
                # Aqui vai chamar o módulo do Aluno D no futuro
                continue
            elif 1 <= text_id <= 100:
                # Por enquanto lê direto do disco
                # (depois vai ser: text = cache.get_text(text_id))
                text = TextManager.load_text(text_id)
                print(f"\n--- Texto {text_id} ---\n")
                print(text[:500] + "...\n")  # Mostra parte do texto
                print("--------------------------\n")
            else:
                print("Número inválido. Digite entre 1 e 100, ou 0/-1.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

if __name__ == "__main__":
    main()
