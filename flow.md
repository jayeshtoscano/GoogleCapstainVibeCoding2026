Flow

                +----------------------+
                |      Client          |
                +----------+-----------+
                           |
                           v
                 POST /gatekeeper
                           |
                           v
                 Gatekeeper Agent
                           |
              Reads agent.md instructions
                           |
              Reads skill.md configuration
                           |
            Creates execution context
                           |
                           v
                LeanContent(prompt)
                           |
                    MongoDB Atlas
        +-----------+-----------+-----------+-----------+
        | Fillers   | Hedges    | Gestures  | Courtesy  |
        +-----------+-----------+-----------+-----------+
                           |
                    Removes unwanted text
                           |
                           v
                 Cleaned Prompt Returned
