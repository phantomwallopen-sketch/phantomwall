from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from detector import detect_risk
from policy import decide_action, sanitize_text

app = FastAPI(title="PhantomWall", version="0.1.0")

class GuardRequest(BaseModel):
    user_input: str
    policy: str | None = "strict"
    context: dict | None = None

class GuardResponse(BaseModel):
    timestamp: str
    risk_score: float
    matches: list[str]
    action: str
    original: str
    output: str

@app.post("/v1/guard", response_model=GuardResponse)
def guard(req: GuardRequest):
    risk, matches = detect_risk(req.user_input, req.context or {})
    action = decide_action(risk, req.policy or "strict")
    out = req.user_input
    if action == "sanitize":
        out = sanitize_text(req.user_input, matches)
    elif action == "block":
        out = "[BLOCKED BY GHOSTGUARD]"
    return GuardResponse(
        timestamp=datetime.utcnow().isoformat() + "Z",
        risk_score=risk,
        matches=matches,
        action=action,
        original=req.user_input,
        output=out,
    )
