"""Shared configuration for NOS API Gateway model and embeddings clients."""

import os

from pydantic import SecretStr

NOS_GATEWAY_BASE_URL = os.getenv(
    "NOS_GATEWAY_BASE_URL",
    "https://api.clg.nos.pt/common/ai/gateway/v1/h2m",
).rstrip("/")
NOS_API_KEY = os.getenv("NOS_API_KEY") or os.getenv("OPENAI_API_KEY")
NOS_CHAT_MODEL = os.getenv("NOS_CHAT_MODEL", "NOS Auto")
NOS_EMBEDDING_MODEL = os.getenv("NOS_EMBEDDING_MODEL", "text-embedding-3-small")


def get_gateway_api_key() -> SecretStr:
    """Return the NOS gateway key as a secret or fail with a safe message."""
    if not NOS_API_KEY:
        raise RuntimeError(
            "Set NOS_API_KEY in the environment or in the local .env file."
        )
    return SecretStr(NOS_API_KEY)
