import logging
import os
import warnings
from typing import Optional

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Silencia logs e avisos
warnings.filterwarnings("ignore")
logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("langchain_google_genai").setLevel(logging.ERROR)
logging.getLogger("rapidocr").setLevel(logging.ERROR)

load_dotenv(find_dotenv())

# Configurações do pipeline para máxima velocidade na CPU
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False               # Desativa OCR
pipeline_options.do_table_structure = False   # Desativa análise pesada de tabelas

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def text_to_md(source: str) -> Optional[str]:
    """Converte um arquivo PDF local ou URL para Markdown via Docling."""
    # Validação de existência para arquivos locais
    if not source.startswith(("http://", "https://")) and not os.path.exists(source):
        print(f"Erro: O arquivo local ou URL '{source}' não foi encontrado.")
        return None

    try:
        print(f"⏳ Processando origem com Docling: {source}...")
        result = converter.convert(source)
        texto_markdown = result.document.export_to_markdown()
        print("✅ Conversão para Markdown concluída.")
        return texto_markdown

    except Exception as e:
        print(f"Erro ao converter documento para Markdown: {e}")
        return None


def ai_request_from_pdf(source: str, prompt: str) -> Optional[str]:
    """Extrai conteúdo de um arquivo PDF local e analisa com o Gemini."""
    if not os.path.exists(source):
        print(f"Erro: O arquivo local '{source}' não foi encontrado.")
        return None

    texto_markdown = text_to_md(source)

    if texto_markdown is None:
        return None

    print("🤖 Enviando conteúdo para o Gemini...")
    final_prompt = f"{prompt}\n\nConteúdo extraído:\n{texto_markdown}"
    resposta = llm.invoke(final_prompt)

    return resposta.content


def ai_request_from_url(url: str, prompt: str) -> Optional[str]:
    """Extrai conteúdo de uma URL e analisa com o Gemini."""
    if not url.startswith(("http://", "https://")):
        print(f"Erro: A URL '{url}' é inválida (deve começar com http:// ou https://).")
        return None

    texto_markdown = text_to_md(url)

    if texto_markdown is None:
        return None

    print("🤖 Enviando conteúdo da URL para o Gemini...")
    final_prompt = f"{prompt}\n\nConteúdo extraído da URL:\n{texto_markdown}"
    resposta = llm.invoke(final_prompt)

    return resposta.content
