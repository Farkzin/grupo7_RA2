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

---

## Aluno B — Cache Base + FIFO - Felipe Simionato Bueno

### Módulos
- `algorithms/cache_base.py`: base do cache (capacidade, armazenamento, métricas, API).
- `algorithms/fifo_cache.py`: política FIFO sobre a base.

### Contrato público (Base)
- `get_text(id:int) -> str`: retorna texto; contabiliza hit/miss e tempo.
- `load(id:int) -> str`: leitura padrão via `TextManager.load_text`.
- Hooks de política:
  - `_on_hit(id:int) -> None`
  - `_insert(id:int, content:str) -> None`

### Armazenamento e limites
- Capacidade fixa: **10** itens (`self.capacity = 10`).
- Estrutura: `self.storage: dict[id -> conteúdo]`.
- Invariante: `len(self.storage) <= 10` garantido em `_insert`.

### Métricas expostas
- `requests`: chamadas totais de `get_text`.
- `hits`: atendidas pela cache.
- `misses`: exigiram leitura.
- `last_time`: duração da última chamada (s).
- `total_time`: soma das durações (s).

### Política FIFO
- Regra: ao inserir no miss e a cache estiver cheia, remove o **mais antigo**.
- Implementação: vetor `self.order: list[int]` preserva a ordem de inserção.
  - Evicção: `victim = self.order.pop(0)` e `storage.pop(victim)`.
  - Hit não reordena.

## Testes

**Objetivo** Verificar funcionalidade do cache base e política FIFO com capacidade fixa de 10, e validar métricas de desempenho.

**Cenário**
- Loader falso para evitar I/O real.
- Inserção de 12 IDs sequenciais para forçar remoção.
- Medição de tempos com loader “lento” (~50 ms por miss).

**Procedimento**
1) Funcional: requisitar IDs 1..12 em sequência.
2) Desempenho: repetir teste com loader que aguarda ~50 ms por leitura; medir `last_time`, `total_time`, média por requisição.

**Resultados observados**
- Funcional:
  - Após 12 requisições com capacidade 10: `requests=12`, `hits=0`, `misses=12`.
  - Conjunto final na cache: IDs `[3..12]` (FIFO removeu 1 e 2), limite de 10 mantido.
- Desempenho:
  - Primeiro miss: `last ≈ 50 ms`.
  - Hit subsequente do mesmo ID: `last ≈ 0–1 ms`.
  - Após 12 requisições com 11 misses: `total ≈ 550 ms`, média ≈ `46 ms/req`.

**Conclusão**
- Evicção FIFO correta (sempre o mais antigo).
- Capacidade respeitada (10).
- Métricas coerentes: misses mais lentos, hits rápidos.