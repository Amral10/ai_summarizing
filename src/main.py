from ai_service import ai_request

# Exemplo 1: Processando um PDF local
resultado_pdf = ai_request("public/relatorio.pdf", "Extraia os 3 pontos principais:")
print("--- Resumo do PDF ---")
print(resultado_pdf)

print("\n" + "=" * 40 + "\n")

# Exemplo 2: Processando uma URL
resultado_url = ai_request("https://mqtt.org", "Resuma o site em uma frase:")
print("--- Resumo do Site ---")
print(resultado_url)
