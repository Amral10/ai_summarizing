from pathlib import Path

from ai_service import ai_request_from_pdf, ai_request_from_url

BASE_DIR = Path(__file__).resolve().parent.parent

caminho_pdf = BASE_DIR / "public" / "relatorio.pdf"

resultado = ai_request_from_pdf(str(caminho_pdf), "Extraia os pontos principais do relatório:")

print("--- Resumo do PDF ---")
print(resultado)


url = "https://mqtt.org/"

resultado_url = ai_request_from_url(url, "Extraia os pontos principais do conteúdo da URL:")

print("--- Resumo da URL ---")
print(resultado_url)
