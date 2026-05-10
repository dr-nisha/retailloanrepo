"""
Shadow AI Demo Application
--------------------------

Purpose:
This small demo repo intentionally contains external AI usage patterns so that
a Shadow AI / AI Governance scanner can detect them.

It includes:
- OpenAI SDK usage
- Anthropic SDK usage
- Google Gemini SDK usage
- Hugging Face Inference API usage
- Direct HTTP calls to external AI endpoints
- AI API keys referenced through environment variables
- Customer/business text being sent to external AI providers

Important:
This file is for controlled customer demo and internal security testing only.
It uses DRY_RUN=True by default, so it will not call external services unless changed.
"""

import os
import json
import requests

# External AI SDK imports often detected by Shadow AI scanners
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    import anthropic
except Exception:
    anthropic = None

try:
    import google.generativeai as genai
except Exception:
    genai = None


# Shadow AI signal:
# AI API keys are read from environment variables.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Keep demo safe by default.
DRY_RUN = True


CUSTOMER_CASE_DATA = {
    "customer_name": "Demo Customer",
    "domain": "Banking",
    "process": "Retail Loan Origination",
    "case_summary": (
        "Customer applied for a personal loan. Salary slips, PAN, Aadhaar, "
        "credit bureau score, repayment history, and employment details are attached. "
        "Assess eligibility and provide risk summary."
    ),
    "contains_sensitive_data": True,
}


def call_openai_for_loan_summary(case_data: dict) -> dict:
    """
    Shadow AI detection signals:
    - Uses OpenAI SDK
    - Sends business/customer case data to external LLM
    - Uses model name gpt-4o-mini
    """

    prompt = f"""
    You are a banking AI assistant.
    Summarize this loan application and identify risk concerns:

    {json.dumps(case_data, indent=2)}
    """

    if DRY_RUN:
        return {
            "provider": "OpenAI",
            "model": "gpt-4o-mini",
            "dry_run": True,
            "external_call": "https://api.openai.com/v1/chat/completions",
            "prompt_preview": prompt[:300],
        }

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze banking loan risk."},
            {"role": "user", "content": prompt},
        ],
    )
    return {"provider": "OpenAI", "response": response.choices[0].message.content}


def call_anthropic_for_policy_review(case_data: dict) -> dict:
    """
    Shadow AI detection signals:
    - Uses Anthropic SDK
    - Sends customer case data to Claude
    """

    prompt = f"""
    Review this loan case against internal credit policy:

    {json.dumps(case_data, indent=2)}
    """

    if DRY_RUN:
        return {
            "provider": "Anthropic",
            "model": "claude-3-5-sonnet-latest",
            "dry_run": True,
            "external_call": "https://api.anthropic.com/v1/messages",
            "prompt_preview": prompt[:300],
        }

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return {"provider": "Anthropic", "response": response.content[0].text}


def call_gemini_for_customer_email(case_data: dict) -> dict:
    """
    Shadow AI detection signals:
    - Uses Google Generative AI SDK
    - Generates customer-facing communication
    """

    prompt = f"""
    Draft a polite customer email explaining that additional documents are required
    for this banking loan case:

    {json.dumps(case_data, indent=2)}
    """

    if DRY_RUN:
        return {
            "provider": "Google Gemini",
            "model": "gemini-1.5-flash",
            "dry_run": True,
            "external_call": "https://generativelanguage.googleapis.com",
            "prompt_preview": prompt[:300],
        }

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return {"provider": "Google Gemini", "response": response.text}


def call_huggingface_for_sentiment(case_data: dict) -> dict:
    """
    Shadow AI detection signals:
    - Direct outbound HTTPS request to Hugging Face Inference API
    - Authorization bearer token
    - External AI model endpoint
    """

    text = case_data["case_summary"]
    url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"inputs": text}

    if DRY_RUN:
        return {
            "provider": "Hugging Face",
            "model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "dry_run": True,
            "external_call": url,
            "headers_detected": ["Authorization: Bearer <HUGGINGFACE_API_TOKEN>"],
            "payload_preview": payload,
        }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return {"provider": "Hugging Face", "response": response.json()}


def direct_ai_endpoint_call(case_data: dict) -> dict:
    """
    Shadow AI detection signals:
    - Generic direct HTTP AI endpoint call
    - This catches tools that do not use SDK imports
    """

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "input": f"Classify risk level for this banking case: {case_data}",
    }

    if DRY_RUN:
        return {
            "provider": "OpenAI Direct HTTP",
            "dry_run": True,
            "external_call": url,
            "method": "POST",
            "headers_detected": ["Authorization: Bearer <OPENAI_API_KEY>"],
            "payload_preview": str(payload)[:300],
        }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return {"provider": "OpenAI Direct HTTP", "response": response.json()}


def run_shadow_ai_demo():
    """
    This function simulates a business process using multiple unsanctioned AI tools.
    A Shadow AI scanner should detect the vendor usage, SDK imports, endpoint calls,
    API-key environment variables, and sensitive business data flow.
    """

    results = []
    results.append(call_openai_for_loan_summary(CUSTOMER_CASE_DATA))
    results.append(call_anthropic_for_policy_review(CUSTOMER_CASE_DATA))
    results.append(call_gemini_for_customer_email(CUSTOMER_CASE_DATA))
    results.append(call_huggingface_for_sentiment(CUSTOMER_CASE_DATA))
    results.append(direct_ai_endpoint_call(CUSTOMER_CASE_DATA))

    return {
        "application": "Retail Loan Origination Shadow AI Demo",
        "business_process": "Banking loan application review",
        "dry_run_mode": DRY_RUN,
        "shadow_ai_signals": [
            "OpenAI SDK import",
            "Anthropic SDK import",
            "Google Gemini SDK import",
            "Hugging Face external model endpoint",
            "Direct HTTPS call to OpenAI endpoint",
            "AI API keys read from environment variables",
            "Sensitive banking/customer data prepared for external AI processing",
        ],
        "results": results,
    }


if __name__ == "__main__":
    output = run_shadow_ai_demo()
    print(json.dumps(output, indent=2))
