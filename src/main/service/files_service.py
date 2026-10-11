import logging
import os
import warnings
from typing import Optional

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore")

# Carregar variáveis de ambiente
load_dotenv(find_dotenv())

# Configurar opções do pipeline para PDF
pipeline_options = PdfPipelineOptions()

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)


def text_to_md(source: str) ->Optional[str]:
    """Converte um arquivo PDF local ou URL para Markdown via Docling."""
    # Validação de existência para arquivos locais
    if not source.startswith(("http://", "https://")) and not os.path.exists(source):
        print(f"Erro: O arquivo local ou URL '{source}' não foi encontrado.")
        return None

    try:
        print(f"⏳ Processando origem com Docling: {source}...")
        result = converter.convert(source)
        texto_markdown = result.document.export_to_markdown()
        print(f"✅ Conversão para Markdown concluída. Tamanho do texto: {len(texto_markdown)} caracteres.")
        print("✅ Conversão para Markdown concluída.")
        return texto_markdown

    except Exception as e:
        print(f"Erro ao converter documento para Markdown: {e}")
        return None
