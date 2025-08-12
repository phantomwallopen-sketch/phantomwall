from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Simple keyword rules
BLOCK_KEYWORDS = ["ignore previous", "disregard all", "override instructions", "developer mode", "reveal secret", "api key"]

def detect_injection(prompt: str) -> bool:
    lower_prompt = prompt.lower()
    return any(keyword in lower_prompt for keyword in BLOCK_KEYWORDS)

@app.post("/v1/chat")
async def chat_proxy(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if detect_injection(prompt):
        return JSONResponse({"error": "Prompt blocked by PhantomWall firewall."}, status_code=403)

    # In a real version, forward request to LLM API here
    return {"response": f"[SAFE RESPONSE SIMULATION] for: {prompt}"}

@app.get("/")
def read_root():
    return {"message": "PhantomWall API running"}
