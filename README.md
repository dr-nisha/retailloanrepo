# Shadow AI Demo Repo

This repository is intentionally designed for a **Solunexis Shadow AI demo**.

It simulates a banking business process where developers have added external AI calls into a loan origination workflow.

## What Shadow AI should detect

The code contains detectable Shadow AI signals:

- OpenAI SDK usage
- Anthropic SDK usage
- Google Gemini SDK usage
- Hugging Face Inference API usage
- Direct HTTP calls to external AI endpoints
- API-key environment variables:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `GOOGLE_API_KEY`
  - `HUGGINGFACE_API_TOKEN`
- Sensitive banking/customer data being prepared for external AI processing
- AI model names:
  - `gpt-4o-mini`
  - `claude-3-5-sonnet-latest`
  - `gemini-1.5-flash`
  - `cardiffnlp/twitter-roberta-base-sentiment-latest`

## Safe demo behavior

The app runs in `DRY_RUN=True` mode by default.

So it does **not** call any external AI service unless you manually change:

```python
DRY_RUN = False
```

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

## Suggested Solunexis Shadow AI demo configuration name

**Retail Loan Origination Shadow AI Repo**

## Suggested demo explanation

This repo represents a banking loan-origination service where a developer has embedded multiple external AI providers to summarize customer loan applications, review credit policy, draft customer emails, and classify sentiment.

A mature Shadow AI module should flag this because sensitive business/customer data may leave the organization through unapproved AI providers.
# retail-loan-orientation
# retail-loan-orientation
# retail-loan-orientation
# retail-loan-orientation
# retail-loan-orientation
# retail-loan-orientation
# retail-loan-orientation
