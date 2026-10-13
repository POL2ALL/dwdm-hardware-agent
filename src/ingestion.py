# Script para processar os PDFs
# src/ingestion.py
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def build_vector_store():
    print("A carregar documentos PDF...")
    loader = PyPDFDirectoryLoader("data/docs/")
    docs = loader.load()
    
    # Text splitter com overlap para não quebrar tabelas e specs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    print(f"A indexar {len(splits)} blocos de texto...")
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory="data/vector_db"
    )
    print("Indexação concluída com sucesso!")

if __name__ == "__main__":
    build_vector_store()