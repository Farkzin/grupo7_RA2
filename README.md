# Projeto RA2 - Algoritmos de Cache

Este projeto implementa um leitor de textos com otimização de leitura via cache.

## Estrutura
- `core/`: base do sistema (Aluno A)
- `algorithms/`: algoritmos de cache (Alunos B, C, D)
- `simulation/`: simulação de performance (Aluno D)
- `texts/`: 100 textos de exemplo

## Execução
```bash
python ra2_main.py

# LRU Cache - Aluno C

## Descricao
Implementacao do algoritmo de substituicao de cache LRU (Least Recently Used) em Python.
Nao usa bibliotecas externas.

## Funcionamento
- O cache armazena ate 10 textos em memoria.
- Cada vez que um texto é acessado, ele é movido para o final da lista de uso.
- Quando o cache enche, o texto menos usado recentemente e removido.
- Os textos sao lidos da pasta texts/ com nome text<ID>.txt.