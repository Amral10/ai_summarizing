# AI Summarizing

Projeto Python que converte uma URL ou um PDF em Markdown com o Docling e envia o conteúdo ao **Gemini 2.5 Flash**, pela integração do LangChain, para gerar um resumo conforme sua instrução.

## Funcionamento atual

`ai_request(source, prompt)` aceita uma URL HTTP/HTTPS ou um caminho local. O serviço chama `DocumentConverter.convert()`, exporta Markdown, concatena a instrução e chama `llm.invoke()`. O resultado é devolvido ao chamador.

Atualmente, **`src/main.py` executa somente o PDF `public/relatorio.pdf`**, com a instrução “Extraia os pontos principais do relatório:”. O caminho do PDF é calculado a partir da localização do script. A URL `https://mqtt.org` aparece neste guia como exemplo separado, não como uma segunda execução automática.

O resumo é impresso no terminal; não há interface web, argumentos de linha de comando ou salvamento automático. A função imprime erros e retorna `None` quando o arquivo não existe ou a conversão/chamada falha. A inicialização do conversor e do cliente Gemini ocorre ao importar o módulo, fora do tratamento de erros da função, e pode interromper a aplicação com traceback.

## Requisitos

- Python 3 com suporte a `venv` e pip.
- Internet para instalação, downloads de modelos do Docling, URLs e API Gemini.
- Chave Gemini obtida no Google AI Studio.
- Memória e espaço em disco para processamento de documentos e modelos auxiliares.

O projeto não declara uma versão mínima própria de Python. A compatibilidade depende das bibliotecas e dos binários disponíveis para seu sistema. O erro relatado ocorreu com Python 3.14.4, mas isso não prova que essa versão é a causa. Python 3.12 pode ser uma alternativa conservadora para investigação; não foi validado aqui com o conjunto completo de dependências.

## 1. Instalar Python

### Debian/Ubuntu

Confira primeiro o sistema e o interpretador:

```bash
cat /etc/os-release
python3 --version
which python3
```

Para instalar os pacotes oferecidos pela distribuição:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Isso instala a versão disponível na sua distribuição, não necessariamente Python 3.12. O suporte `python3-venv` serve ao Python padrão da distribuição; um Python instalado separadamente pode precisar de suporte fornecido por seu próprio instalador. Não substitua o Python do sistema nem use repositórios de outra distribuição. Consulte o [guia Python do Debian](https://wiki.debian.org/Python).

### Outra versão de Python, sem substituir a do sistema

Se precisar testar Python 3.12, uma alternativa é instalar `uv` conforme a [documentação oficial](https://docs.astral.sh/uv/getting-started/installation/). Depois, na raiz do projeto e sem uma `.venv` já existente:

```bash
uv python install 3.12
uv venv --python 3.12 --seed .venv
source .venv/bin/activate
```

Essa criação substitui o passo `python3 -m venv .venv` abaixo. `--seed` inclui pip. Consulte também o [gerenciamento de Python com uv](https://docs.astral.sh/uv/guides/install-python/).

### Windows/macOS

Use os [instaladores oficiais do Python](https://www.python.org/downloads/) e escolha uma versão compatível com as dependências. Confira `py --version` no Windows ou `python3 --version` no macOS. Os comandos de ambiente virtual para Windows estão na seção 3.

## 2. Clonar e entrar na raiz do projeto

Clone o repositório usando sua URL. Substitua `<URL_DO_REPOSITORIO>` pelo endereço de clonagem:

```bash
git clone <URL_DO_REPOSITORIO> ai_summarizing
cd ai_summarizing
```

Se já tiver uma cópia local, entre na pasta onde salvou o projeto. Confira se está na raiz:

```bash
pwd
ls src/main.py requirements.txt public/relatorio.pdf
```

Todos os exemplos seguintes partem da raiz de `ai_summarizing`.

## 3. Criar e conferir a .venv

Linux/macOS, usando o Python escolhido:

```bash
python3 -m venv .venv
source .venv/bin/activate
which python3
python3 -m pip --version
python3 -c 'import sys; print("Executável:", sys.executable); print("Ambiente virtual:", sys.prefix != sys.base_prefix)'
```

O `python3` deve apontar para `.venv/bin/python3`, o pip deve estar em `.venv/.../site-packages`, e a última linha deve mostrar `True`. **O texto `(.venv)` no prompt não garante um ambiente válido.** A diferença entre `sys.prefix` e `sys.base_prefix` é a verificação descrita na [documentação de venv](https://docs.python.org/3/library/venv.html).

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip --version
python -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
```

Se o PowerShell bloquear a ativação, use diretamente `.\.venv\Scripts\python.exe` nos comandos. No Prompt de Comando, ative com `.venv\Scripts\activate.bat`. Não é necessário mudar políticas globais para usar o executável do ambiente.

Ative o ambiente novamente em cada terminal novo. Para sair, execute `deactivate`.

## 4. Instalar todas as dependências

Somente depois de validar a `.venv`, execute:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip check
```

No Windows, use `python` no lugar de `python3`, ou o caminho direto do Python da `.venv`.

Dependências diretas presentes no projeto:

| Biblioteca | Versão fixada | Finalidade |
| --- | --- | --- |
| `docling` | `2.134.0` | Conversão de documentos/URLs e exportação para Markdown. |
| `langchain-google-genai` | `4.4.0` | Cliente `ChatGoogleGenerativeAI` para Gemini. |
| `python-dotenv` | `1.2.4` | Localização e carregamento das variáveis do `.env`. |

O pip instala também as dependências transitivas necessárias. Entre as relacionadas ao erro de PDF estão `torch` (PyTorch), `torchvision` e `transformers`. O conjunto completo depende do Python, plataforma e resolução de dependências: `requirements.txt` não fixa todo o ambiente. Para ver **todas as bibliotecas realmente instaladas**:

```bash
python3 -m pip list
python3 -m pip show docling langchain-google-genai python-dotenv torch torchvision transformers
```

`logging`, `os`, `warnings`, `typing` e `pathlib` fazem parte da biblioteca padrão de Python e não precisam de pip. Não atualize pacotes isolados sem conferir compatibilidade.

## 5. Configurar o Gemini

1. Acesse [Google AI Studio — API Keys](https://aistudio.google.com/app/apikey).
2. Crie uma chave para um projeto disponível, seguindo o fluxo apresentado. Consulte as [instruções oficiais](https://ai.google.dev/gemini-api/docs/api-key).
3. Se ainda não tiver `.env`, copie o exemplo:

```bash
cp .env.example .env
```

No PowerShell, use `Copy-Item .env.example .env`. Não sobrescreva um `.env` já configurado.

Abra o arquivo em um editor e substitua o exemplo:

```dotenv
GEMINI_API_KEY=sua_chave_real_aqui
```

Não compartilhe a chave em conversas, capturas de tela ou logs. O código usa `load_dotenv(find_dotenv())`, e o cliente Gemini lê a configuração do ambiente. A integração LangChain dá prioridade a `GOOGLE_API_KEY`, com `GEMINI_API_KEY` como alternativa, conforme a [documentação oficial da integração](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai). Variáveis antigas exportadas no terminal podem prevalecer; o carregamento padrão do dotenv não substitui variáveis já existentes. Revise isso sem imprimir valores secretos.

O `.gitignore` já contém `.env` e `.venv/`. Confira sem mostrar a chave:

```bash
git check-ignore .env
git ls-files .env
```

O primeiro deve mostrar que o arquivo é ignorado; o segundo não deve listar `.env` como rastreado. Se a chave já entrou no Git, ignorar o arquivo não apaga o histórico: retire-o do rastreamento e revogue a chave exposta no AI Studio.

**ChatGPT Plus não cobre a API Gemini.** São serviços e cobranças separados. O Gemini oferece faixa gratuita sujeita a disponibilidade e limites; não significa acesso ilimitado. Confira [faturamento](https://ai.google.dev/gemini-api/docs/billing/) e [cotas atuais](https://ai.google.dev/gemini-api/docs/rate-limits) antes de habilitar pagamentos.

## 6. Executar o PDF

Com o ambiente ativo e a chave configurada, na raiz:

```bash
python3 src/main.py
```

O programa lê `public/relatorio.pdf` e imprime `--- Resumo do PDF ---` seguido da resposta. Se ocorrer um erro tratado, pode imprimir `None`. O comando faz uma chamada real à API e envia o conteúdo extraído ao Google.

A primeira conversão pode baixar modelos auxiliares do Docling e demorar. Para outro documento, substitua o PDF no caminho esperado ou adapte o caminho e prompt no seu código. PDFs corrompidos, protegidos por senha ou com estrutura incomum podem falhar.

## 7. Exemplos de URL e PDF

Os comandos abaixo são para bash/zsh no Linux/macOS, executados da raiz. `PYTHONPATH=src` torna o módulo importável. Ambos fazem chamadas reais ao Gemini.

### URL

```bash
PYTHONPATH=src python3 - <<'PY'
from ai_service import ai_request

resumo = ai_request("https://mqtt.org", "Resuma este site em uma frase.")
print(resumo)
PY
```

### PDF com outra instrução

```bash
PYTHONPATH=src python3 - <<'PY'
from ai_service import ai_request

resumo = ai_request("public/relatorio.pdf", "Resuma este relatório em cinco tópicos.")
print(resumo)
PY
```

Também é possível salvar um exemplo em `src/`, importar `ai_request` da mesma forma e executá-lo da raiz. Caminhos relativos passados diretamente à função dependem da pasta atual; o `main.py` usa um caminho absoluto calculado.

O teste próprio de `python3 src/ai_service.py` procura `relatorio.pdf` **na pasta atual**, sem `public/`. Prefira `python3 src/main.py` ou os exemplos acima para o PDF existente.

## Estrutura

```text
ai_summarizing/
├── public/
│   └── relatorio.pdf       # PDF existente
├── src/
│   ├── ai_service.py       # Conversão e chamada Gemini
│   └── main.py             # Exemplo atual de PDF
├── requirements.txt        # Dependências diretas
├── .env.example            # Modelo sem segredo
├── .env                    # Criado localmente; ignorado
├── .venv/                  # Criada localmente; ignorada
├── .gitignore
└── README.md
```

## Solução dos erros observados

### `python: command not found` mesmo com `(.venv)`

Fora de uma `.venv`, algumas distribuições fornecem apenas `python3`. Dentro do ambiente, confira os caminhos da seção 3. Não crie um alias para o Python do sistema para mascarar o problema. Use `python3` somente depois de confirmar que ele pertence à `.venv`.

### PEP 668: `externally-managed-environment`

Esse erro indica uma tentativa de instalar em um ambiente protegido pela distribuição. Mesmo que `(.venv)` apareça no prompt, esse erro pode ocorrer se o Python/pip não estiverem efetivamente usando um ambiente virtual válido. Não use `sudo pip`, `--break-system-packages` nem remova a proteção do sistema.

Na raiz, preserve a `.venv` antiga e recrie:

```bash
deactivate 2>/dev/null || true
mv .venv .venv-backup
python3 -m venv .venv
source .venv/bin/activate
which python3
python3 -m pip --version
python3 -c 'import sys; print(sys.prefix != sys.base_prefix)'
```

Execute o `mv` apenas se `.venv` existir e `.venv-backup` não existir; caso contrário, pule ou escolha um nome de backup livre. O backup não está coberto pelo `.gitignore` atual: não o adicione ao Git. Depois de os caminhos e o resultado `True` confirmarem o ambiente, instale:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip check
```

Se o shell insistir em outro executável, abra um terminal novo ou use `.venv/bin/python3 -m pip ...` diretamente. Se `venv` falhar por falta de `ensurepip`, instale o suporte correspondente ao Python escolhido: para o Python padrão Debian/Ubuntu, normalmente `python3-venv`; para Python externo, siga seu instalador. Ambientes copiados ou movidos devem ser recriados.

### PDF: `AutoImageProcessor` e `torchvision::nms`

A mensagem sobre `AutoImageProcessor` ocultava uma falha anterior ao importar `torchvision`:

```text
RuntimeError: operator torchvision::nms does not exist
```

As versões observadas eram `torch 2.14.1+cpu`, `torchvision 0.29.1`, `transformers 5.18.0` e `docling 2.134.0`, com Python 3.14.4. Esses dados registram o erro; não constituem um conjunto recomendado ou validado. O resumo de URL funcionou, mas isso não confirma o funcionamento do PDF, que usa outros componentes de extração.

Comece com diagnóstico sem chamar a API:

```bash
python3 --version
which python3
python3 -m pip --version
python3 -m pip show torch torchvision transformers docling
python3 -m pip check
python3 -c 'import torch; print(torch.__version__); import torchvision; print(torchvision.__version__)'
python3 -c 'from transformers import AutoImageProcessor; print("Importação OK")'
```

Leia o traceback inteiro. `pip check` não testa o carregamento de extensões binárias. A falta de `nms` pode envolver binários incompatíveis, instalação incompleta ou builds CPU/CUDA inadequados; a mensagem sozinha não identifica a causa.

Para recuperação:

1. Registre as versões e o traceback antes de alterar pacotes.
2. Confira o par `torch`/`torchvision` e o suporte ao Python na [matriz oficial](https://github.com/pytorch/vision#installation).
3. Prefira reproduzir a instalação numa `.venv` nova, preservando o ambiente antigo. Se faltarem binários para seu Python, teste uma versão compatível separadamente.
4. Se precisar reparar PyTorch, obtenha o comando no [seletor oficial](https://pytorch.org/get-started/locally/) para seu sistema e plataforma: CPU para execução sem GPU; CUDA apenas quando houver suporte apropriado. Execute com o pip da `.venv`, escolhendo versões compatíveis de `torch` e `torchvision`, sem misturar builds ou atualizar somente um deles.
5. Repita os testes de importação e `pip check`. Reinstalar pode corrigir uma instalação danificada, mas **não garante** resolver incompatibilidade ou defeito dos pacotes. Não mude os pins do projeto por tentativa sem registrar e avaliar o motivo.

Após as importações funcionarem, isole a conversão do PDF, sem importar o serviço nem chamar Gemini:

```bash
python3 - <<'PY'
from docling.document_converter import DocumentConverter

result = DocumentConverter().convert("public/relatorio.pdf")
markdown = result.document.export_to_markdown()
print("Conversão OK; caracteres extraídos:", len(markdown))
PY
```

O teste pode baixar modelos do Docling. Depois de a conversão passar, execute `python3 src/main.py` se desejar enviar o conteúdo ao Gemini. Se continuar falhando, preserve o traceback completo para investigar junto aos projetos envolvidos.

## Outros problemas

| Sintoma | Verificação |
| --- | --- |
| `No module named ...` | Python e pip da mesma `.venv`, instalação completa; para `ai_service`, use `PYTHONPATH=src` ou script em `src/`. |
| `No matching distribution found` | Python, arquitetura, índice usado e disponibilidade da versão fixada; não remova pins automaticamente. |
| Chave ausente/inválida | `.env` na raiz, chave ativa, ausência de variável antiga com prioridade. Não imprima o segredo. |
| HTTP 429 / limite atingido | Cotas do projeto no AI Studio; aguarde renovação e reduza chamadas. Outra chave do mesmo projeto não garante outra cota. |
| Modelo indisponível | Disponibilidade de `gemini-2.5-flash` para seu projeto e condições atuais do Google. |
| Arquivo ausente | PDF existente e pasta atual nos caminhos relativos; main.py espera public/relatorio.pdf. |
| URL falha | Endereço, conexão e bloqueios do site; páginas com autenticação/JavaScript podem não ser extraídas como no navegador. |
| Primeira execução lenta | Downloads de modelos, internet, memória, espaço e permissões do cache. |
| Resposta `None` | A função tratou uma falha; leia a mensagem anterior e corrija a causa. |
| Documento muito grande | Todo o Markdown vai em uma requisição; o código não divide documentos em partes. Reduza a fonte ou implemente divisão para respeitar limites. |

## Segurança e limitações

O conteúdo extraído é enviado ao Google. Processe apenas documentos que você tenha autorização para usar e confira as condições do serviço para dados sensíveis. Resumos podem conter erros ou omissões; compare com a fonte quando a precisão importar.

Mantenha `.env` fora do Git, preserve `.env.example` sem segredo e revogue chaves expostas. A aplicação não oferece processamento totalmente local: a extração é local, mas o resumo usa a API Gemini.
