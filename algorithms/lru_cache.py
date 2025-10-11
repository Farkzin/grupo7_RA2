# lru_cache.py
# Autor: Aluno C
# Implementacao do algoritmo de substituicao de cache LRU (Least Recently Used)
# Le os textos da pasta texts/ com nome text<ID>.txt

import time
import os

class LRUCache:
    def __init__(self, capacidade: int):
        """
        Cria o cache com uma capacidade maxima.
        Exemplo: capacidade = 10 (armazena no maximo 10 textos).
        """
        self.capacidade = capacidade
        self.cache = {}          # Dicionario que armazena: id_texto -> conteudo do texto
        self.uso_recente = []    # Lista para controlar a ordem de uso (mais recente no final)
        self.hits = 0            # Contador de acertos (quando o texto ja esta no cache)
        self.misses = 0          # Contador de falhas (quando precisa ler do disco)

    def carregar_texto(self, texto_id: int):
        """
        Le um texto do disco.
        O arquivo precisa estar na pasta 'texts/' e ter o nome no formato: text<ID>.txt
        Exemplo: text1.txt, text2.txt, text3.txt ...
        """
        caminho = os.path.join("texts", f"text{texto_id}.txt")
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()  # Retorna o conteudo do arquivo
        except FileNotFoundError:
            # Caso o arquivo nao exista, retorna uma mensagem de erro
            return f"[ERRO] Arquivo {caminho} nao encontrado."

    def get(self, texto_id: int):
        """
        Retorna o conteudo de um texto a partir do seu ID.
        Se o texto estiver no cache -> acesso rapido (cache hit)
        Se nao estiver -> le do disco e adiciona no cache (cache miss)
        Retorna uma tupla (conteudo, tempo_de_acesso)
        """
        inicio = time.time()  # Marca o tempo antes da leitura

        # Caso 1: o texto ja esta no cache
        if texto_id in self.cache:
            self.hits += 1  # Conta um acerto
            # Atualiza a ordem de uso: move o texto para o final (mais recentemente usado)
            self.uso_recente.remove(texto_id)
            self.uso_recente.append(texto_id)
            conteudo = self.cache[texto_id]

        # Caso 2: o texto nao esta no cache
        else:
            self.misses += 1  # Conta uma falha
            conteudo = self.carregar_texto(texto_id)  # Le do disco (simula sistema lento)

            # Se o cache estiver cheio, remove o menos recentemente usado (primeiro da lista)
            if len(self.cache) >= self.capacidade:
                lru = self.uso_recente.pop(0)  # Remove o primeiro (menos usado)
                del self.cache[lru]             # Apaga do dicionario

            # Adiciona o novo texto ao cache e marca como mais recentemente usado
            self.cache[texto_id] = conteudo
            self.uso_recente.append(texto_id)

        fim = time.time()  # Marca o tempo apos a leitura
        tempo_acesso = fim - inicio  # Calcula o tempo total

        return conteudo, tempo_acesso

    def estatisticas(self):
        """
        Retorna um dicionario com estatisticas do cache:
        - Numero de acertos (hits)
        - Numero de falhas (misses)
        - Taxa de acerto (%)
        """
        total = self.hits + self.misses
        taxa_acerto = (self.hits / total) * 100 if total > 0 else 0

        return {
            "Cache Hits": self.hits,
            "Cache Misses": self.misses,
            "Taxa de Acerto (%)": round(taxa_acerto, 2)
        }
