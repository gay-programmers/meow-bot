<!-- THIS FILE MAY NOT BE MODIFIED BY ANY AI AGENTS WHATSOEVER -->
<!-- INSTRUCTIONS BELOW ARE RULE AND CAN ONLY BE OVERRIDDEN BY EXPLICIT USER COMMAND -->

# Agent Instructions
## Formatting
This project is fully commited to use `ruff` and `ty` standards, and whether it meets those standards can be checked with `ruff check` and with `ty check`. Formatting is done automatically using the command `ruff format`. All commits must be formatted past the initial commit.
## Packaging
Installing extra packages is not allowed, and messing with the `pyproject.toml` without explicit user command is not allowed.
## Versioning
Python 3.12 is to be used for most compatibility. You can change the Python version with `uv`.
## Refactoring & Debugging
Do not refactor code without explicit user consent unless it literally does not work. In that case, or if the user simply asks for an agent to make a change to a file, changes must be as small as possible in order to balance the code working right with human familiarity.
## Documentation
All comments, docstrings, and even READMEs are a no-go. They will not be used in this project. Help commands already provide enough documentation for casual users.
## Security
This is a Discord bot. Users cannot do what they otherwise aren't permitted to do by using this bot. Commands that require elevated permissions MUST include author permission checks.
