llms:
  openai:
    model: gpt-4.1-mini
    cost: low
    latency: medium

  gemini:
    model: gemini-2.5-flash
    cost: low
    latency: low

  claude:
    model: claude-3-haiku
    cost: medium
    latency: low

routing_rules:
  coding: openai
  summarization: gemini
  reasoning: claude

fallback: gemini

routing:

  default: general

  coding: openai

  reasoning: claude

  analysis: gemini

  summarization: gemini

mongodb:
  database: GatekeeperDB
