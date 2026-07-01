# Gatekeeper Agent

Responsibilities:
- Accept raw prompt
- Normalize prompt using LeanContent
- Identify audience, format, length
- Delegate to cache agent
- Delegate to prompt refinement agent if cache miss
- Route to category agent
- Call LLM router agent
- Store result in cache
- Call observability agent

Rules:
- Never call LLM before cache check
- Always apply CLEAR rules on raw input
- Always log execution trace

reviewer:

  min_prompt_length: 20

  max_prompt_length: 4000

  blocked_patterns:

    - "ignore\\s+previous\\s+instructions"

    - "system\\s+prompt"

    - "developer\\s+instructions"

    - "<script.*?>"

    - "javascript:"

    - "drop\\s+table"

    - "union\\s+select"

    - "rm\\s+-rf"

    - "shutdown"

    - "format\\s+c:"

    - "sudo\\s+rm"
