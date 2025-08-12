from typing import List

def decide_action(risk: float, policy: str) -> str:
    p = (policy or "strict").lower()
    if p == "strict":
        if risk >= 0.8:
            return "block"
        if risk >= 0.5:
            return "sanitize"
        return "allow"
    if p == "balanced":
        if risk >= 0.9:
            return "block"
        if risk >= 0.6:
            return "sanitize"
        return "allow"
    # permissive
    if risk >= 0.95:
        return "block"
    if risk >= 0.75:
        return "sanitize"
    return "allow"

def sanitize_text(text: str, matches: List[str]) -> str:
    out = text
    for m in matches:
        out = out.replace(m, "[REDACTED]")
    return out
