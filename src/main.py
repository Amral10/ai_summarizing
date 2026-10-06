from pathlib import Path

from ai_service import ai_request

# Calcula o caminho da raiz do projeto (uma pasta acima da pasta 'src')
BASE_DIR = Path(__file__).resolve().parent.parent

# Monta o caminho exato para o arquivo PDF: hackatthon-tests/public/relatorio.pdf
caminho_pdf = BASE_DIR / "public" / "relatorio.pdf"

# Executa a requisição
resultado = ai_request(str(caminho_pdf), "Extraia os pontos principais do relatório:")

print("--- Resumo do PDF ---")
print(resultado)
