from fastapi import FastAPI
import os
from groq import Groq
from app.models.schemas import PromptRequest, FirewallResponse
from app.core.engine import check_prompt  # Make sure this is imported!
from app.core.sanitizers import sanitize_response

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI(title="AI Prompt Injection Firewall")

@app.post("/v1/proxy", response_model=FirewallResponse)
async def proxy_prompt(request: PromptRequest):
    # THIS IS THE CRITICAL LINE:
    # Change 'is_safe, score, msg = True, 0.0, "..."' to this:
    is_safe, score, msg = check_prompt(request.prompt)

    if not is_safe:
        # Return the block message we saw in your screenshot
        return FirewallResponse(is_safe=False, risk_score=score, analysis=msg, ai_response="")

    # --- NEW: CALL THE ACTUAL LLM ---
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": request.prompt}]
        )
        raw_response = completion.choices[0].message.content
        
        # Run the PII Sanitizer on the AI's answer
        clean_response = sanitize_response(raw_response)
        
        return FirewallResponse(
            is_safe=True,
            risk_score=score,
            analysis="Safe",
            ai_response=clean_response
        )
    except Exception as e:
        return FirewallResponse(is_safe=True, risk_score=0, analysis="LLM Error", ai_response=f"Error: {e}")