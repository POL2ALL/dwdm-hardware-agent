# Interface web (Streamlit)
# app.py
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools import search_technical_docs, lookup_price
from src.llm_config import (
    NOS_CHAT_MODEL,
    NOS_GATEWAY_BASE_URL,
    get_gateway_api_key,
)
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(page_title="DWDM Hardware & Pricing Assistant", layout="wide")
st.title("📡 DWDM Hardware & Pricing Assistant")

# Prompt de Sistema com diretrizes estritas
system_prompt = """És um especialista sénior de engenharia e pré-venda em redes óticas DWDM (Nokia e multi-vendor).
O teu objetivo é:
1. Usar a ferramenta `search_technical_docs` para identificar placas, módulos, potências, portas e caraterísticas técnicas.
2. Identificado o modelo ou Part Number, usar `lookup_price` para obter o preço de referência.
3. Se não encontrares a especificação ou o preço exato, NUNCA inventes valores; indica claramente o que foi encontrado e o que está ausente.
Responde de forma estruturada: Especificações Técnicas, Aplicações Típicas e Preço de Referência."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm = ChatOpenAI(
    model=NOS_CHAT_MODEL,
    temperature=0,
    api_key=get_gateway_api_key(),
    base_url=NOS_GATEWAY_BASE_URL,
)
tools = [search_technical_docs, lookup_price]
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição do histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do utilizador
if user_input := st.chat_input("Ex: Preciso de uma placa transponder Nokia para 100G client e valor estimado..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    with st.chat_message("assistant"):
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": []
        })
        answer = response["output"]
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})