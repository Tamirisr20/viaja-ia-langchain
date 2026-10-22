import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

BASE = Path(__file__).parent
PASTA_DOCS = BASE / "documentos"
PASTA_INDICE = BASE / "indice_faiss"

modelo = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    api_key=api_key,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

if PASTA_INDICE.exists():
    vetores = FAISS.load_local(
        str(PASTA_INDICE), embeddings, allow_dangerous_deserialization=True
    )
else:
    arquivos = sorted(PASTA_DOCS.glob("*.pdf"))
    documentos = sum([PyPDFLoader(str(a)).load() for a in arquivos], [])
    pedacos = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100
    ).split_documents(documentos)
    vetores = FAISS.from_documents(pedacos, embeddings)
    vetores.save_local(str(PASTA_INDICE))

dados_recuperados = vetores.as_retriever(search_kwargs={"k": 4})

prompt_consulta_seguro = ChatPromptTemplate.from_messages([
    ("system", "Responda usando exclusivamente o conteúdo fornecido. "
               "Se a resposta não estiver no contexto, diga que não encontrou "
               "nos documentos. Não invente."),
    ("human", "{query}\n\nContexto: \n{contexto}\n\nResposta:")
])

cadeia = prompt_consulta_seguro | modelo | StrOutputParser()


def responder(pergunta: str):
    trechos = dados_recuperados.invoke(pergunta)
    contexto = "\n\n".join(
        f"[{Path(t.metadata['source']).name}] {t.page_content}" for t in trechos
    )
    return cadeia.invoke({"query": pergunta, "contexto": contexto})


if __name__ == "__main__":
    print(responder("Como devo proceder caso tenha um item comprado roubado e caso eu tenha o cartão gold"))