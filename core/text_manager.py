import os
import time

class TextManager:
    @staticmethod
    def load_text(text_id: int) -> str:
        path = os.path.join("texts", f"text{text_id}.txt")
        if not os.path.exists(path):
            return f"Erro: texto {text_id} não encontrado."

        # simular latência de disco proporcional ao tamanho do arquivo
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        return content
