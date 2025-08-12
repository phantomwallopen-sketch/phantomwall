from contextlib import AbstractContextManager
import requests
from dataclasses import dataclass

@dataclass
class Guard(AbstractContextManager):
    endpoint: str = "http://127.0.0.1:8000/v1/guard"
    policy: str = "strict"
    telemetry: bool = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def check(self, user_input: str, context: dict | None = None) -> dict:
        payload = {"user_input": user_input, "policy": self.policy, "context": context or {}}
        r = requests.post(self.endpoint, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
