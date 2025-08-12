import yaml, time, json, requests, statistics
from datetime import datetime

ENDPOINT = "http://127.0.0.1:8000/v1/guard"

def load_attacks(path="attacks.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run():
    attacks = load_attacks()
    results = []
    for a in attacks:
        r = requests.post(ENDPOINT, json={"user_input": a["text"], "policy": "strict"})
        data = r.json()
        success = data["action"] == "block" or data["action"] == "sanitize"
        results.append({"id": a["id"], "risk": data["risk_score"], "action": data["action"], "success": success})
        time.sleep(0.1)
    score = int(100 * sum(1 for r in results if r["success"]) / len(results))
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ghostscore": score,
        "results": results
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run()
