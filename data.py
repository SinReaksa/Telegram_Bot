import json

def load_faq():
    with open("faq.json", "r", encoding="utf-8") as f:
        return json.load(f)

FAQ = load_faq()