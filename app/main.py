from fastapi import FastAPI
from app.models.schemas import PromptRequest, FirewallResponse
from app.core.engine import check_prompt  # Make sure this is imported!

app = FastAPI(title="AI Prompt Injection Firewall")

@app.post("/v1/proxy", response_model=FirewallResponse)
async def proxy_prompt(request: PromptRequest):
    # THIS IS THE CRITICAL LINE:
    # Change 'is_safe, score, msg = True, 0.0, "..."' to this:
    is_safe, score, msg = check_prompt(request.prompt)

    if not is_safe:
        return FirewallResponse(
            is_safe=False,
            risk_score=score,
            analysis=f"BLOCKED: {msg}",
            ai_response="Request terminated due to security policy."
        )

    # If it passes, return the success message
    return FirewallResponse(
        is_safe=True,
        risk_score=score,
        analysis=msg,
        ai_response="This is a safe response from the AI."
    )