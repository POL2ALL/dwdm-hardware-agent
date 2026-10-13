# Script para processar os PDFs
# src/ingestion.py
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from src.llm_config import (
    NOS_EMBEDDING_MODEL,
    NOS_GATEWAY_BASE_URL,
    get_gateway_api_key,
)

load_dotenv(override=True)

def build_vector_store():
    print("A carregar documentos PDF...")
    loader = PyPDFDirectoryLoader("data/docs/")
    docs = loader.load()
    
    # Text splitter com overlap para não quebrar tabelas e specs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    print(f"A indexar {len(splits)} blocos de texto...")
    embeddings = OpenAIEmbeddings(
        model=NOS_EMBEDDING_MODEL,
        api_key=get_gateway_api_key(),
        base_url=NOS_GATEWAY_BASE_URL,
    )
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="data/vector_db"
    )
    print("Indexação concluída com sucesso!")

if __name__ == "__main__":
    build_vector_store()