name: LeanContentSkill

description: >
  Removes conversational noise before prompts are sent to LLMs.

mongodb:
  connection_string: mongodb+srv://<username>:<password>@cluster.mongodb.net/
  database: PromptCleaning
  collections:
    fillers: fillers
    hedges: hedges
    gestures: gestures
    courtesy: courtesy

settings:
  lowercase: false
  trim_spaces: true
  remove_duplicate_spaces: true
