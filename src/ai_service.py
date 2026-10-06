import logging
import os
import warnings
from typing import Optional

from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Silencia logs e avisos
warnings.filterwarnings("ignore")
logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("langchain_google_genai").setLevel(logging.ERROR)
logging.getLogger("rapidocr").setLevel(logging.ERROR)

load_dotenv()

# Instanciados uma única vez no módulo
converter = DocumentConverter()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def ai_request(source: str, prompt: str) -> Optional[str]:
    """Extrai o conteúdo de uma URL ou PDF local e analisa com o Gemini."""
    if not source.startswith(("http://", "https://")) and not os.path.exists(source):
        print(f"Erro: O arquivo local '{source}' não foi encontrado.")
        return None

    try:
        result = converter.convert(source)
        texto_markdown = result.document.export_to_markdown()

        final_prompt = f"{prompt}\n\nConteúdo extraído:\n{texto_markdown}"
        resposta = llm.invoke(final_prompt)

        return resposta.content

    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return None


# Executado APENAS se você rodar "python3 ai_service.py"
if __name__ == "__main__":
    print("Testando o módulo localmente...")
    resumo = ai_request("relatorio.pdf", "Resuma este arquivo:")
    print(resumo)
