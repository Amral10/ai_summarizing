from pathlib import Path

from ai_service import ai_request

BASE_DIR = Path(__file__).resolve().parent.parent

caminho_pdf = BASE_DIR / "public" / "relatorio.pdf"

resultado = ai_request(str(caminho_pdf), "Extraia os pontos principais do relatório:")

print("--- Resumo do PDF ---")
print(resultado)
