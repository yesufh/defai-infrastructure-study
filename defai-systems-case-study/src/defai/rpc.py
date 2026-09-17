from typing import Any

import httpx

from .config import settings


class SolanaRPC:
    """Small read-only Solana JSON-RPC client."""

    def __init__(self, rpc_url: str | None = None):
        self.rpc_url = rpc_url or settings.rpc_url

    def _request(self, method: str, params: list[Any]) -> Any:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        response = httpx.post(
            self.rpc_url,
            json=payload,
            timeout=settings.request_timeout,
        )
        response.raise_for_status()

        body = response.json()
        if "error" in body:
            raise RuntimeError(body["error"])

        return body["result"]

    def get_signatures_for_address(
        self,
        address: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")

        return self._request(
            "getSignaturesForAddress",
            [address, {"limit": limit}],
        )

    def get_transaction(
        self,
        signature: str,
    ) -> dict[str, Any] | None:
        return self._request(
            "getTransaction",
            [
                signature,
                {
                    "encoding": "jsonParsed",
                    "maxSupportedTransactionVersion": 0,
                },
            ],
        )

    def get_balance(self, address: str) -> int:
        result = self._request("getBalance", [address])
        return result["value"]
