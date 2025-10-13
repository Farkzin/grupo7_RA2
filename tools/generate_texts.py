import os
os.makedirs("texts", exist_ok=True)
base = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50)  # ~50 frases
for i in range(1, 101):
    content = f"Texto {i}\n\n" + (base + " ") * 20  # ajusta para >1000 palavras
    with open(os.path.join("texts", f"text{i}.txt"), "w", encoding="utf-8") as f:
        f.write(content)
print("100 textos gerados em /texts/")
