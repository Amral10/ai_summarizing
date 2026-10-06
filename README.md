# AI Summarizing

Projeto Python para extrair o conteúdo de arquivos PDF ou páginas da web e gerar resumos usando o Google Gemini. A extração é feita pelo [Docling](https://github.com/docling-project/docling) e a chamada ao modelo é feita pelo LangChain.

## Requisitos

- Python 3.11 ou superior
- `pip`
- Acesso à internet para instalar as dependências, acessar URLs e chamar a API
- Uma chave da API do Google Gemini

> O Docling pode baixar modelos auxiliares na primeira execução. Reserve espaço em disco e aguarde alguns minutos nessa primeira inicialização.

## Instalação

### 1. Obtenha o projeto

Clone o repositório ou copie a pasta para o computador e entre nela:

```bash
git clone <URL_DO_REPOSITORIO> ai_summarizing
cd ai_summarizing
```

Se o projeto já estiver salvo localmente, apenas execute `cd` apontando para a pasta `ai_summarizing`.

### 2. Crie um ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (Prompt de Comando):

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instale as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure a chave do Gemini

Crie uma chave no [Google AI Studio](https://aistudio.google.com/app/apikey). Depois, copie o arquivo de exemplo:

Linux/macOS:

```bash
cp .env.example .env
```

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

Abra `.env` e substitua o valor de `GEMINI_API_KEY` pela sua chave real:

```env
GEMINI_API_KEY=sua_chave_real
```

Não compartilhe nem faça commit do arquivo `.env`.

## Como executar

Com o ambiente virtual ativado e a chave configurada:

```bash
python main.py
```

O programa executa dois exemplos:

1. Lê `public/relatorio.pdf` e extrai os três pontos principais.
2. Acessa `https://mqtt.org` e resume o site em uma frase.

Também é possível executar o módulo de serviço diretamente:

```bash
python ai_service.py
```

## Usando o serviço no próprio código

```python
from ai_service import ai_request

resumo = ai_request(
    "public/relatorio.pdf",
    "Resuma este documento em cinco tópicos.",
)
print(resumo)
```

O primeiro argumento pode ser:

- um caminho para um arquivo local compatível com o Docling, como `public/relatorio.pdf`;
- uma URL iniciada por `http://` ou `https://`.

O segundo argumento é a instrução enviada ao Gemini junto com o conteúdo extraído.

## Estrutura do projeto

```text
ai_summarizing/
├── public/
│   └── relatorio.pdf      # PDF usado pelo exemplo local
├── src/
│   └── main.py            # Exemplos de execução
│   └── ai_service.py      # Extração de conteúdo e chamada ao Gemini
├── requirements.txt       # Dependências Python diretas
├── .env.example           # Modelo de configuração da API
└── README.md              # Este guia
```

## Solução de problemas

- **`GEMINI_API_KEY` não configurada:** confirme que existe um arquivo `.env` na raiz do projeto e que a variável contém uma chave válida.
- **Arquivo local não encontrado:** execute o comando na raiz do projeto e confirme o caminho informado. No exemplo, `public/relatorio.pdf` deve existir.
- **Falha ao acessar uma URL:** verifique a conexão, o endereço e se o site permite acesso automatizado.
- **Primeira execução lenta:** o Docling pode baixar modelos de OCR e processamento de documentos antes de gerar o primeiro resultado.
- **Comando `python` não encontrado:** no Linux/macOS, tente `python3`; no Windows, tente `py`.

## Segurança

A chave da API deve ficar somente em `.env`. O arquivo já está listado no `.gitignore`; se uma chave real tiver sido publicada ou compartilhada, revogue-a no Google AI Studio e gere outra.
