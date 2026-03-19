"""Symptom assessment assistant: structured, safety-first questioning flow.

This module implements a simple state machine for collecting symptoms,
performing immediate safety screening, asking adaptive follow-up questions,
and returning cautious, non-diagnostic guidance.

Outputs are JSON-serializable dicts with keys like:
- type: 'question' | 'result' | 'emergency'
- text: message to show
- choices: optional list of choices for multiple-choice questions
- context: updated context dict to send back on next call

Note: This is a lightweight implementation intended for server-side use
within the chat app. It must NOT provide diagnoses and always includes a
disclaimer in responses.
"""
from typing import Dict, Any, List
import re

DISCLAIMER = "This information is not a medical diagnosis and does not replace professional medical advice."


RED_FLAGS = [
    r"chest pain",
    r"severe difficulty breathing|difficulty breathing|shortness of breath|can't breathe|cant breathe",
    r"loss of consciousness|passed out|fainted",
    r"severe bleeding|bleeding heavily|bleeding profusely",
    r"confusion|disoriented|seizure|seizures",
    r"sudden weakness on one side|weakness on one side|slurred speech",
]


def text_has_red_flag(text: str) -> List[str]:
    found = []
    t = text.lower()
    for pattern in RED_FLAGS:
        if re.search(pattern, t):
            found.append(pattern)
    return found


COMMON_SYMPTOMS = [
    "fever", "cough", "sore throat", "shortness of breath", "breath", "chest pain",
    "headache", "nausea", "vomiting", "diarrhea", "abdominal pain", "dizziness",
    "weakness", "fatigue", "rash", "bleeding", "confusion",
]


def extract_symptoms(text: str) -> List[str]:
    t = text.lower()
    found = []
    for s in COMMON_SYMPTOMS:
        if s in t:
            found.append(s)
    # also quick capture numbers/fever temp
    m = re.search(r"(\b\d{2,3}(?:\.\d)?°?\s?(c|f)\b)", text.lower())
    if m:
        found.append("reported_temperature")
    return list(dict.fromkeys(found))


def make_question(text: str, choices: List[str] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
    return {
        "type": "question",
        "text": text,
        "choices": choices or [],
        "context": context or {}
    }


def make_emergency(text: str) -> Dict[str, Any]:
    return {
        "type": "emergency",
        "text": text + "\n\n" + DISCLAIMER,
        "context": {}
    }


def make_result(text: str, details: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": "result",
        "text": text + "\n\n" + DISCLAIMER,
        "details": details,
        "context": {}
    }


def start_assessment(user_text: str) -> Dict[str, Any]:
    # Initial symptom extraction and safety screen
    red = text_has_red_flag(user_text)
    if red:
        return make_emergency(
            "Some of the information you provided suggests a possible medical emergency (e.g., chest pain or severe difficulty breathing). Please seek immediate medical care or call your local emergency number."
        )

    symptoms = extract_symptoms(user_text)
    context = {
        "stage": "duration",
        "symptoms": symptoms,
        "answers": {
            "initial_text": user_text
        }
    }

    return make_question(
        "Thank you — how long have you had these symptoms?",
        choices=["Less than 24 hours", "1-3 days", "More than 3 days", "Ongoing / Chronic"],
        context=context
    )


def handle_answer(context: Dict[str, Any], user_text: str) -> Dict[str, Any]:
    stage = context.get("stage", "duration")
    answers = context.get("answers", {})

    # Normalize input
    t = user_text.strip()

    # Stage machine
    if stage == "duration":
        answers["duration"] = t
        context["stage"] = "severity"
        context["answers"] = answers
        return make_question(
            "How would you rate the severity of your main symptom right now?",
            choices=["Mild (doesn't limit activity)", "Moderate (some limitation)", "Severe (greatly limits activity)"],
            context=context
        )

    if stage == "severity":
        answers["severity"] = t
        context["stage"] = "progression"
        context["answers"] = answers
        return make_question(
            "Is the symptom getting better, worse, or staying the same?",
            choices=["Getting better", "Getting worse", "About the same"],
            context=context
        )

    if stage == "progression":
        answers["progression"] = t
        context["stage"] = "associated"
        context["answers"] = answers
        return make_question(
            "Are you experiencing any of the following? (choose all that apply)",
            choices=["Fever", "Cough", "Vomiting", "Diarrhea", "Dizziness", "Rash", "None of the above"],
            context=context
        )

    if stage == "associated":
        # accept comma-separated choices
        choices = [c.strip() for c in re.split(r"[,;]", t) if c.strip()]
        answers["associated"] = choices
        context["stage"] = "age_gender"
        context["answers"] = answers
        return make_question(
            "What's the patient's age? (you can enter a number)",
            choices=None,
            context=context
        )

    if stage == "age_gender":
        answers["age_gender"] = t
        context["stage"] = "chronic"
        context["answers"] = answers
        return make_question(
            "Does the patient have any chronic conditions (e.g., diabetes, heart disease), or is pregnant?",
            choices=["No", "Yes - diabetes", "Yes - heart disease", "Yes - pregnant", "Other / prefer not to say"],
            context=context
        )

    if stage == "chronic":
        answers["chronic"] = t
        # Prepare a cautious reasoning summary
        context["answers"] = answers
        # Build possible explanations using simple rules
        possible = []
        somewhat = []
        less = []

        sym = context.get("symptoms", [])
        assoc = [a.lower() for a in answers.get("associated", [])]
        sev = answers.get("severity", "").lower()

        # Simple rules
        if any(k in assoc for k in ["fever", "cough"]) or any(s in sym for s in ["fever", "cough"]):
            possible.append({
                "name": "Infectious respiratory illness (e.g., common cold, influenza, other viral infections)",
                "why": "Fever or cough reported",
                "typical_symptoms": ["fever", "cough", "sore throat", "body aches"]
            })

        if any(s in sym for s in ["chest pain"]) or any(k in answers.get("initial_text", "").lower() for k in ["chest pain", "shortness of breath"]):
            possible.append({
                "name": "Cardiac or serious pulmonary causes (e.g., angina, pulmonary embolism)",
                "why": "Chest pain or breathlessness mentioned",
                "typical_symptoms": ["chest pain", "shortness of breath", "sweating", "lightheadedness"]
            })

        if any(s in sym for s in ["abdominal pain"]) or any(k in assoc for k in ["vomiting", "diarrhea"]):
            somewhat.append({
                "name": "Gastrointestinal causes (e.g., gastroenteritis, food-related upset)",
                "why": "Abdominal symptoms or vomiting/diarrhea",
                "typical_symptoms": ["abdominal pain", "nausea", "vomiting", "diarrhea"]
            })

        if any(s in sym for s in ["weakness"]) or "slurred" in answers.get("initial_text", "").lower():
            somewhat.append({
                "name": "Neurological causes to consider (e.g., stroke-like symptoms)",
                "why": "Weakness or slurred speech mentioned",
                "typical_symptoms": ["sudden weakness on one side", "difficulty speaking", "facial droop"]
            })

        if not possible and not somewhat:
            less.append({
                "name": "Non-specific viral illness or minor self-limited condition",
                "why": "Symptoms do not clearly point to a serious condition",
                "typical_symptoms": ["mild fever", "fatigue", "body aches"]
            })

        guidance = {
            "more_consistent": possible,
            "somewhat_consistent": somewhat,
            "less_consistent": less,
            "what_to_do_now": []
        }

        # Self-care suggestions (general, cautious)
        guidance["what_to_do_now"].append("Stay hydrated and rest as needed.")
        guidance["what_to_do_now"].append("Use over-the-counter symptom relief per local guidance; do not take medications without consulting a provider if you are unsure.")

        # When to seek care
        urgency = []
        if sev and "severe" in sev:
            urgency.append("Symptoms described as severe — consider urgent medical evaluation.")

        urgency.append("Seek immediate care if any emergency signs develop: chest pain, severe difficulty breathing, sudden weakness, severe bleeding, loss of consciousness.")

        details = {
            "answers": answers,
            "guidance": guidance,
            "urgency_notes": urgency
        }

        text = "Based on the information provided, here are some possible explanations and next steps (not a diagnosis):"
        return make_result(text, details)

    # Fallback
    return make_question("Can you tell me more about the symptom?", choices=None, context=context)


def process(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point. Expects payload with keys:
    - action: 'start' or 'answer'
    - text: user-provided text
    - context: optional context dict from previous response
    """
    action = payload.get("action", "start")
    text = (payload.get("text") or "").strip()
    context = payload.get("context") or {}

    if action == "start":
        return start_assessment(text)

    # Safety screen on every message
    if text:
        red = text_has_red_flag(text)
        if red:
            return make_emergency(
                "Some responses suggest a possible emergency. Please seek immediate medical attention."
            )

    # If no context, start
    if not context:
        return start_assessment(text)

    # Otherwise handle answer flow
    return handle_answer(context, text)
