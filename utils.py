import re
from difflib import get_close_matches
from data import FAQ


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[?។!.,;:\"'(){}\[\]]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def find_answer(text: str):

    text = normalize(text)

    # 1. exact match
    for item in FAQ:
        if normalize(item["question"]) == text:
            return item["answer"]

    # 2. keyword match
    for item in FAQ:
        if all(k in text for k in item["keywords"]):
            return item["answer"]

    # 3. fuzzy match
    questions = [item["question"] for item in FAQ]

    match = get_close_matches(text, questions, n=1, cutoff=0.5)

    if match:
        for item in FAQ:
            if item["question"] == match[0]:
                return item["answer"]

    return None