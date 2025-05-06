from transformers import pipeline

_loaded_models = {}

def get_summarizer(model_name: str):
    if model_name not in _loaded_models:
        _loaded_models[model_name] = pipeline("summarization", model=model_name)
    return _loaded_models[model_name]

def chunk_text(text, max_words=300):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words])

def generate_summary(text, model_name="sshleifer/distilbart-cnn-12-6"):
    summarizer = get_summarizer(model_name)
    chunks = list(chunk_text(text, max_words=250))
    summaries = []

    for i, chunk in enumerate(chunks):
        try:
            result = summarizer(
                chunk,
                max_length=60,
                min_length=50,
                do_sample=False
            )
            if result and 'summary_text' in result[0]:
                clean_text = result[0]['summary_text'].strip().replace('\n', ' ')
                for bad_phrase in ["he says", "she says", "says the", "he adds", "she adds", "he warns", "she warns"]:
                    clean_text = clean_text.replace(bad_phrase, "")
                clean_text = clean_text.replace('"', '').replace("'", '')
                if any(x in clean_text.lower() for x in [
                    "we will see", "if we let", "it's a very", "we must", "we should"
                ]):
                    continue  # Skip hallucinated chunks
                summaries.append(f"🔹 **Section {i + 1}:** {clean_text}\n")

        except Exception as e:
            summaries.append(f"[Skipped section due to error: {e}]")

    return "\n\n".join(summaries) if summaries else "⚠️ Summary failed."
