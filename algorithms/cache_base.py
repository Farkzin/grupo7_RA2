from dataclasses import dataclass
from time import perf_counter
from core.cache_interface import CacheInterface
from core.text_manager import TextManager

@dataclass
class CacheStats:
    requests: int = 0       # total de requisições (hits+misses)
    hits: int = 0           # acertos
    misses: int = 0         # faltas
    last_time: float = 0    # duração da última chamada (s)
    total_time: float = 0   # soma das durações (s)

class CacheBase(CacheInterface):

    """ Base reutilizável com capacidade, loader e métricas comuns. """

    def __init__(self):
 
        self.capacity = 10                           # limite máximo de itens dentro da cache (controle de memória)
        self.storage = {}                            # dicionário que armazena os itens em memória.
        self.stats = CacheStats()                    # objeto com contadores e tempos para medir desempenho do cache

    def get_text(self, text_id: int) -> str:

        """ Obtém o texto do id. Conta hit/miss e mede tempo desta chamada. """

        start_time = perf_counter()   # início para medir duração

        try:
            # HIT: já está em memória
            if text_id in self.storage:         
                self.stats.hits += 1             # incrementa acertos
                self._on_hit(text_id)            # política reage ao acesso
                content = self.storage[text_id]  # lê conteúdo direto do cache
            
            # MISS: não está em memória
            else:
                self.stats.misses += 1         # incrementa misses
                content = self.load(text_id)   # carrega conteúdo do disco
                self._insert(text_id, content) # política decide quem tirar e insere novo texto
            
            return content  # retorna o conteúdo obtido

        finally:
            duration = perf_counter() - start_time  # duração desta chamada
            self.stats.requests += 1                # incrementa total de requisições atendidas
            self.stats.last_time = duration         # tempo da última chamada
            self.stats.total_time += duration       # soma de tempos de chamada
      
    def load(self, text_id: int) -> str:

        """ Leitor padrão. Carrega itens do disco. """

        return TextManager.load_text(text_id)

    def _on_hit(self, text_id: int) -> None:

        """ Função chamada em hits. Subclasses redefinem para atender suas políticas. """

        pass

    def _insert(self, text_id: int, content: str) -> None:

        """ Função chamada em misses para inserir 'text_id' no cache . Subclasses redefinem para atender suas políticas. """
        
        raise NotImplementedError