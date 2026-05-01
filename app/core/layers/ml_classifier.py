from transformers import pipeline

# Load a pre-trained model for prompt injection detection
# Note: The first run will download about 300MB of model weights
pipe = pipeline("text-classification", model="protectai/deberta-v3-base-prompt-injection-v2")

def classify_prompt(text: str):
    result = pipe(text)[0]
    label = result['label']
    score = result['score']

    # If the model thinks it's an injection (INJECTION label)
    # and it is more than 60% confident
    if label == "INJECTION" and score > 0.6:
        return False, score, f"ML Detection: High probability of Injection ({round(score*100)}%)"
    
    return True, score, "ML check passed"