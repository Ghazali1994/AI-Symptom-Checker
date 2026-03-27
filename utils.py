import json

# Load rules from rules.json
with open("rules.json") as f:
    RULES = json.load(f)

# Red-flag symptoms
RED_FLAGS = [
    "chest pain",
    "severe shortness of breath",
    "confusion",
    "high fever",
    "severe bleeding"
]

def check_red_flags(symptoms):
    """
    Check if any red-flag symptoms are present.
    Returns: (bool, message)
    """
    for flag in RED_FLAGS:
        if flag in symptoms:
            return True, f"Red flag detected: {flag}. Seek emergency medical care immediately!"
    return False, None

def evaluate_conditions(symptoms):
    """
    Evaluate all conditions in RULES based on selected symptoms.
    Returns a sorted list of conditions with matched symptoms count.
    """
    results = []
    for condition in RULES.get("conditions", []):
        match_count = len(set(symptoms) & set(condition.get("symptoms", [])))
        if match_count > 0:
            results.append({"condition": condition["name"], "matches": match_count})
    # Sort descending by number of matched symptoms
    results.sort(key=lambda x: x["matches"], reverse=True)
    return results

def next_question(selected_symptoms, asked_questions):
    """
    Determine the next symptom to ask about for interactive questioning.
    Returns: {"symptom": symptom_name, "question": question_text} or None if done.
    """
    # Build a flat list of all symptoms from all conditions
    all_symptoms = set()
    for condition in RULES.get("conditions", []):
        all_symptoms.update(condition.get("symptoms", []))

    # Ask only symptoms that haven't been selected or asked yet
    for symptom in all_symptoms:
        question_text = f"Do you have {symptom.replace('_', ' ')}?"
        if symptom not in selected_symptoms and question_text not in asked_questions:
            return {"symptom": symptom, "question": question_text}

    # No more questions to ask
    return None

def most_likely_condition(symptoms):
    """
    Returns the single most likely condition based on symptoms.
    Handles tie-breakers by choosing the condition with the highest match count.
    """
    results = evaluate_conditions(symptoms)
    if results:
        return max(results, key=lambda x: x["matches"])
    return None
