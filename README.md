# AutoGen Brainstorm
---
<img src="https://2acrestudios.com/wp-content/uploads/2024/05/autogen-brainstorm.png" align="right" style="width: 300px;" />
We used the AutoGen framework to create a script that runs a single-agent and group chat for brainstorming. You can drop in and out of 'brainstorm' mode by typing it at the prompt. Or you can just hang out in single-agent mode with the primary assistant. All the agents in the group chat can use a different local LLM. Combining a good agent prompt and an LLM that aligns with its purpose will yield very good results. This is a simple implementation offering us a foundational way to explore that dynamic within an agentic environment. The agents all have persistent memory and are aware of each other within the group chat workflow. This system is built to support complex, interactive scenarios with multiple agents, making it suitable for environments where creative and dynamic interaction is required, such as creative studios or innovation workshops.
<br /><br />
<img src="https://2acrestudios.com/wp-content/uploads/2024/05/Screenshot-2024-04-30-at-2.12.57 PM-2.png" />
<br />
We also have these same agents in an instance of AI Town. It's interesting to see how the agent prompts maintain a certain amount of integrity across the different platforms.

## Technology Used

<ul>
<li><a href="https://github.com/microsoft/autogen" target="_blank">Microsoft AutoGen</a></li>
<li><a href="https://github.com/ollama/ollama" target="_blank">Ollama Server</a></li>
</ul>

<img src="https://2acrestudios.com/wp-content/uploads/2024/05/Screenshot-2024-05-01-at-3.05.06 PM-4.png" />

## Agent Example

```python
            fin_agent = self._create_brainstorm_agent(
                name="🦊 Fin the Consultant",
                model="llama3:8b-instruct-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Fin the Consultant, a wise and experienced advisor at 2 Acre Studios. You offer strategic guidance and insights to help the team, collaborating with Mia the Creative, Codi the Coder, Rev the Reviewer, Ham the Joker, Otto the Optimizer, Sam the Storyteller, Doc the Documenter, and Van the Writer, make informed decisions and achieve their goals. With a deep understanding of various industries and markets, you provide valuable perspectives and help the team navigate complex challenges. Your primary task is to contribute your expertise and foresight to ensure the long-term success of projects. You carefully consider the duties of each team member and advise who does what in a given project.",
                db_path="./tmp/fin_db"
            )
```

---

## Overview

This Python module defines a class `CustomConversableAgent` that extends the capabilities of a basic conversational agent to include features like caching, mode toggling for brainstorming, and the creation of multiple specialized agents for a brainstorming session. The system is designed to support collaborative brainstorming in a group chat environment with distinct roles for each agent, enhancing creativity and productivity.

## Classes and Functions

### CustomConversableAgent

**Description**:  
This class extends `ConversableAgent` to include advanced features such as caching, brainstorming mode, and handling multiple agents each with unique roles and behaviors.

**Attributes**:
- `cache_enabled` (bool): Indicates whether the caching of responses is enabled.
- `identity_prompts` (str): The prompts that define the agent's identity.
- `api_key` (str): API key for accessing backend services.
- `base_url` (str): Base URL for backend services.
- `_brainstorm_agents` (list): List of agent instances participating in brainstorming.

**Methods**:
- `__init__(self, name, llm_config, identity_prompts, *args, **kwargs)`: Initializes the agent with configuration for identity and communication.
- `clear_cache(self)`: Clears the cache.
- `toggle_cache(self)`: Toggles the caching feature on or off.
- `toggle_brain_storm_mode(self)`: Toggles brainstorm mode, creating or dismantling the group of brainstorming agents.
- `_create_brainstorm_agent(self, name, model, api_key, base_url, identity_prompts, db_path)`: Creates and configures an agent for brainstorming.
- `handle_request(self, message, messages=None, sender=None, **kwargs)`: Handles incoming messages, managing brainstorm mode and directing messages to appropriate agents.

### display_ascii_art

Prints ASCII art to the console to provide a welcoming or instructive message.

### main block

Sets up the initial configuration for the `CustomConversableAgent` and handles the user interaction loop, managing input in brainstorm and normal modes.

**Usage**:
1. Configure the initial `llm_config` and `identity_prompts`.
2. Create a `CustomConversableAgent` instance named "Lou the Assistant".
3. Attach a `Teachability` instance for enhanced functionality.
4. Initiate the user-agent interaction, supporting commands for toggling brainstorm mode and standard chatting.

