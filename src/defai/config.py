import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    rpc_url: str = os.getenv(
        "SOLANA_RPC_URL",
        "https://api.mainnet-beta.solana.com",
    )
    request_timeout: float = float(os.getenv("REQUEST_TIMEOUT", "20"))


settings = Settings()
