import os

class TextManager:
    @staticmethod
    def load_text(text_id: int) -> str:
        """Carrega um texto do disco a partir do número."""
        path = os.path.join("texts", f"text{text_id}.txt")

        if not os.path.exists(path):
            return f"Erro: texto {text_id} não encontrado."

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        return content
