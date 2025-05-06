import re

def highlight_entities(text, entities):
    flat_entities = []
    for label, items in entities.items():
        for phrase in items:
            if phrase == "I":  # Filter again here
                continue
            flat_entities.append((phrase, label))

    flat_entities.sort(key=lambda x: len(x[0]), reverse=True)

    for phrase, label in flat_entities:
        escaped_phrase = re.escape(phrase)
        pattern = rf'\b{escaped_phrase}\b'
        style = "background-color:#ffea00; color:#000000; padding:2px 4px; border-radius:4px;"
        replacement = f"<span style='{style}'>{phrase}</span>"
        text = re.sub(pattern, replacement, text)

    return text
