from transformers import pipeline
from collections import defaultdict

ner_pipeline = pipeline("ner", grouped_entities=True)

def clean_token(text):
    return text.replace("##", "")

def extract_entities(text):
    raw_entities = ner_pipeline(text)
    grouped = defaultdict(set)

    for ent in raw_entities:
        label = ent["entity_group"] if "entity_group" in ent else ent["entity"]
        word = clean_token(ent["word"])
        grouped[label].add(word)

    return dict(grouped)
