# 🧳 ViajaIA

Assistente de viagens e consulta de documentos feito com **LangChain**, **LangGraph** e **Groq**.
O projeto reúne, em scripts independentes, os principais conceitos do ecossistema LangChain:
cadeias (LCEL), saídas estruturadas, chat com memória, roteamento com grafos e RAG sobre PDFs.

> Projeto de estudo, desenvolvido a partir do curso *LangChain e Python: criando ferramentas
> com a OpenAI* (Alura), adaptado para usar a API da Groq.

## O que cada parte faz

| Arquivo | O que faz |
|---|---|
| `main.py` | Encadeia 3 cadeias: interesse → cidade (JSON) → restaurantes (JSON) → atividades culturais |
| `mainchat.py` | Chat com o guia "Sr. Passeios" que lembra do que foi dito na conversa |
| `mainLangGraph.py` | Grafo que classifica a pergunta e a encaminha para o especialista certo (praia ou montanha) |
| `main_rag.py` | RAG: responde perguntas com base em PDFs, sem inventar o que não está neles |
| `app.py` | Interface de chat em Streamlit para o RAG |

## Tecnologias

- Python 3.12
- LangChain e LangGraph
- Groq (modelo `openai/gpt-oss-120b`)
- Embeddings Hugging Face (`paraphrase-multilingual-MiniLM-L12-v2`)
- FAISS (índice vetorial)
- Streamlit

## Como instalar

Recomendado: Python 3.11 ou 3.12.

```powershell
git clone https://github.com/SEU_USUARIO/viaja-ia-langchain.git
cd viaja-ia-langchain
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate`.

## Configuração

1. Crie uma chave de API gratuita em [console.groq.com](https://console.groq.com).
2. Copie o arquivo de exemplo e preencha com a sua chave:

```powershell
Copy-Item .env.example .env
```

```
GROQ_API_KEY=sua_chave_aqui
```

Opcional: adicione `DEBUG=true` ao `.env` para ver cada passo interno das cadeias no terminal.

3. Para usar o RAG, coloque os seus PDFs na pasta `documentos/`. Os PDFs usados no
   desenvolvimento (condições de seguro de cartões Mastercard Gold, Platinum e Standard)
   não estão incluídos no repositório.

## Como rodar

```powershell
python main.py              # cadeias encadeadas
python mainchat.py          # chat com memória
python mainLangGraph.py     # roteamento com LangGraph
python main_rag.py          # RAG no terminal
streamlit run app.py --server.fileWatcherType none   # interface web
```

Na primeira execução do RAG, o modelo de embeddings é baixado e os PDFs são indexados.
O índice fica salvo em `indice_faiss/`, então as próximas execuções são bem mais rápidas.
Se você trocar os PDFs, apague essa pasta para reindexar.

O `--server.fileWatcherType none` evita uma enxurrada de avisos no terminal causados
pela biblioteca `transformers`.

## Exemplo de uso

Pergunta feita ao RAG:

> Como devo proceder caso tenha um item comprado roubado e caso eu tenha o cartão gold?

O assistente responde com os passos, documentos exigidos e limites de cobertura que
constam nos PDFs. Para perguntas fora dos documentos, ele informa que não encontrou a
informação, em vez de inventar uma resposta.

<!-- Adicione aqui um print ou GIF da interface: ![Demonstração](docs/demo.gif) -->

## Estrutura do projeto

```
viaja-ia-langchain/
├── documentos/          # seus PDFs (não versionados)
├── indice_faiss/        # índice gerado automaticamente (não versionado)
├── app.py
├── main.py
├── main_rag.py
├── mainchat.py
├── mainLangGraph.py
├── requirements.txt     # dependências diretas do projeto
├── requirements.lock.txt  # versões exatas do ambiente de desenvolvimento
├── .env.example
└── .gitignore
```

## Próximos passos

- [ ] Guardar o histórico do chat em SQLite, para a conversa sobreviver ao fechar o programa
- [ ] Dar memória ao grafo do LangGraph
- [ ] Criar um agente com ferramentas (clima, orçamento de viagem)
- [ ] Mostrar na interface de qual PDF e página veio cada resposta

## Segurança

O arquivo `.env` com a sua chave de API nunca deve ser enviado ao GitHub. Ele já está no `.gitignore`.