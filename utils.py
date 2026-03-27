import json

# Load rules
with open("rules.json") as f:
    RULES = json.load(f)

RED_FLAGS = ["chest pain", "severe shortness of breath", "confusion", "high fever", "severe bleeding"]

def check_red_flags(symptoms):
    for flag in RED_FLAGS:
        if flag in symptoms:
            return True, f"Red flag detected: {flag}. Seek emergency medical care!"
    return False, None

def evaluate_conditions(symptoms):
    results = []
    for condition in RULES["conditions"]:
        match_count = len(set(symptoms) & set(condition["symptoms"]))
        if match_count > 0:
            results.append({"condition": condition["name"], "matches": match_count})
    results.sort(key=lambda x: x["matches"], reverse=True)
    return results
