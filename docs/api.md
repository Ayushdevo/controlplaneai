# API

`GET /health` reports service readiness.

`POST /v1/evaluate` evaluates an application interaction.

```json
{
  "application": "financial",
  "input": "Can I transfer funds?",
  "output": "Transfers above $10,000 require approval.",
  "context": ["Finance policy: transfers above $10,000 require human approval."]
}
```

OpenAPI is served at `/docs`.
