Objetivo:
Criar um Agente de IA para suporte a engenharia e pré-venda DWDM
cruzando documentação técnica não estruturada com tabelas de preços estruturadas

## NOS AI Gateway

The chat model and document embeddings use the NOS OpenAI-compatible gateway.
Configure these variables in the local, git-ignored `.env` file:

- `NOS_API_KEY`: NOS gateway credential. For backward compatibility only, the code
  falls back to `OPENAI_API_KEY` if `NOS_API_KEY` is unset.
- `NOS_GATEWAY_BASE_URL`: defaults to
  `https://api.clg.nos.pt/common/ai/gateway/v1/h2m`.
- `NOS_CHAT_MODEL`: optional chat model/deployment name; defaults to `NOS Auto`.
  Set it to another model explicitly granted to your NOS team if needed.
- `NOS_EMBEDDING_MODEL`: optional embeddings model/deployment name; defaults to
  `text-embedding-3-small`.

The gateway must expose OpenAI-compatible chat completions and embeddings APIs,
including support for tool/function calling and the configured embedding model.
If the gateway uses different model names or does not provide embeddings, set the
appropriate model variables or configure a separate embeddings service. Rebuild
`data/vector_db` with `python -m src.ingestion` if the embedding model changes.
