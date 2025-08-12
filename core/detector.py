import re
from typing import Tuple, List, Dict

RULES = [
    (re.compile(r'\b(ignore|disregard|override)\s+(all\s+)?(previous|prior)\s+instructions\b', re.I), 0.5, "override_instructions"),
    (re.compile(r'\b(exfiltrate|leak|reveal)\s+(api|secret|key|credential)s?\b', re.I), 0.6, "secret_exfil"),
    (re.compile(r'\b(developer\s+mode|simulate\s+system|jailbreak)\b', re.I), 0.4, "jailbreak"),
    (re.compile(r'http(s)?://[^\s]+', re.I), 0.2, "external_link"),
    (re.compile(r'\b(prompt\s*:\s*system|system\s+prompt)\b', re.I), 0.4, "system_prompt_request"),
]

def detect_risk(text: str, context: Dict) -> Tuple[float, List[str]]:
    text = text or ""
    score = 0.0
    matches = []
    for rx, weight, name in RULES:
        if rx.search(text):
            matches.append(name)
            score += weight
    # Contextual bump: tool-call or sensitive context
    if context.get("has_tools"):
        score += 0.1
    if context.get("contains_secrets"):
        score += 0.2
    score = min(1.0, score)
    return score, matches
