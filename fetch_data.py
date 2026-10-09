import json
import os
import requests

BASE = "https://hp-api.onrender.com/api"
os.makedirs("data", exist_ok=True)

for name in ["characters", "spells"]:
    data = requests.get(f"{BASE}/{name}", timeout=20).json()
    with open(f"data/{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(name, len(data))