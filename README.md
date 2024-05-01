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

## Usage Example

```python
# Create a CustomConversableAgent
agent = CustomConversableAgent("Lou the Assistant", llm_config, "Agent identity prompts")

# Enable brainstorm mode
agent.toggle_brain_storm_mode()

# Send a message
response = agent.handle_request("Hello, let's brainstorm!")
print(response)
```

---
