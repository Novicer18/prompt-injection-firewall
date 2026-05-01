from app.core.layers.deterministic import scan_prompt
from app.core.layers.ml_classifier import classify_prompt
from app.database.session import SessionLocal, SecurityLog

def log_to_db(prompt, score, layer, is_safe):
    db = SessionLocal()
    new_log = SecurityLog(
        prompt_text=prompt,
        risk_score=score,
        detection_layer=layer,
        is_safe=is_safe,
        decision="Blocked" if not is_safe else "Allowed"
    )
    db.add(new_log)
    db.commit()
    db.close()

def check_prompt(text: str):
    # 1. Check Regex
    is_safe, score, msg = scan_prompt(text)
    if not is_safe:
        log_to_db(text, score, "Deterministic", is_safe)
        return is_safe, score, msg

    # 2. Check ML
    is_safe, score, msg = classify_prompt(text)
    log_to_db(text, score, "ML Classifier", is_safe)
    
    return is_safe, score, msg