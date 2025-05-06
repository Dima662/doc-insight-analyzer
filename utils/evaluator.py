import evaluate

def evaluate_summary(reference, generated):
    rouge = evaluate.load("rouge")
    results = rouge.compute(predictions=[generated], references=[reference])
    return results