llms:

  openai:
    model: gpt-4.1
    enabled: true

  gemini:
    model: gemini-2.5-flash
    enabled: true

  claude:
    model: claude-sonnet-4
    enabled: true


##########################################################
# POLICY ENGINE
##########################################################

policies:

  default:

    providers:
      - gemini
      - openai
      - claude

    rules:

      keyword:
        "refactor": openai
        "optimize": claude
        "debug": openai

      complex_prompt_threshold: 2000
      complex_provider: claude

    fallback: gemini


  coding:

    providers:
      - openai
      - claude

    rules:

      keyword:
        "leetcode": openai
        "fix bug": openai
        "performance": claude

      complex_prompt_threshold: 1500
      complex_provider: claude

    fallback: openai


  reasoning:

    providers:
      - claude
      - openai

    rules:

      keyword:
        "why": claude
        "explain": claude

      complex_prompt_threshold: 1200
      complex_provider: claude

    fallback: claude


  analysis:

    providers:
      - gemini
      - claude

    rules:

      keyword:
        "trend": gemini
        "summary": gemini

      complex_prompt_threshold: 1800
      complex_provider: claude

    fallback: gemini
