# Ferramentas do agente (procura técnica e preço)
# src/tools.py
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from src.llm_config import (
    NOS_EMBEDDING_MODEL,
    NOS_GATEWAY_BASE_URL,
    get_gateway_api_key,
)

# 1. Ferramenta de Procura Técnica
@tool
def search_technical_docs(query: str) -> str:
    """Pesquisa especificações técnicas, portas, capacidade e compatibilidade de hardware DWDM nos manuais."""
    embeddings = OpenAIEmbeddings(
        model=NOS_EMBEDDING_MODEL,
        api_key=get_gateway_api_key(),
        base_url=NOS_GATEWAY_BASE_URL,
    )
    vector_store = Chroma(
        persist_directory="data/vector_db",
        embedding_function=embeddings,
    )
    results = vector_store.similarity_search(query, k=4)
    return "\n\n".join([doc.page_content for doc in results])

# 2. Ferramenta de Procura de Preço
@tool
def lookup_price(part_number_or_keyword: str) -> str:
    """Procura o preço de referência e descrição exata na price list a partir do Part Number ou código de equipamento."""
    try:
        # Carrega ficheiro Excel ou CSV
        df = pd.read_excel("data/prices/price_list.xlsx")  # ou pd.read_csv(...)
        
        # Procura sem case-sensitive em colunas de P/N ou Descrição
        mask = (
            df['Part_Number'].astype(str).str.contains(part_number_or_keyword, case=False, na=False) |
            df['Description'].astype(str).str.contains(part_number_or_keyword, case=False, na=False)
        )
        matches = df[mask][['Part_Number', 'Description', 'List_Price', 'Currency']].head(5)
        
        if matches.empty:
            return f"Nenhum artigo encontrado para: {part_number_or_keyword}"
        return matches.to_string(index=False)
    except Exception as e:
        return f"Erro ao consultar lista de preços: {str(e)}"