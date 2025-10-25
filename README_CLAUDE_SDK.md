# AutoGen Brainstorm - Claude Agent SDK Edition

<img src="https://2acrestudios.com/wp-content/uploads/2024/05/autogen-brainstorm.png" align="right" style="width: 300px;" />

A collaborative AI brainstorming framework powered by the **Claude Agent SDK**, featuring specialized agents, custom skills, and automated workflows.

This version reimagines the original AutoGen brainstorming system using Anthropic's Claude Agent SDK, bringing advanced agentic capabilities including:

- 🤖 **Subagents** for specialized tasks
- 🎯 **Skills** for reusable brainstorming capabilities
- 🔗 **Hooks** for automated workflows
- 💬 **Interactive CLI** for seamless collaboration

---

## 🌟 What's New in the Claude SDK Version

### Powered by Claude Sonnet 4.5
- Latest Claude model with enhanced reasoning and creativity
- More natural and contextual conversations
- Better code understanding and generation

### Agent Architecture
- **9 Specialized Brainstorming Agents** each with unique expertise
- **Subagent System** for parallel task execution
- **Skill-based Capabilities** for reusable workflows
- **Hook System** for quality control and automation

### Features
- ✨ Single-agent mode (Lou the Assistant) for focused work
- 🎨 Group brainstorming mode with all 9 agents
- 📝 Automatic session logging and summaries
- 🔍 Quality checks on all responses
- 🛠️ Built-in skills: Ideation, Code Review, Storytelling

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/2acrestudios/autogen-brainstorm.git
   cd autogen-brainstorm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your Anthropic API key
   # ANTHROPIC_API_KEY=your-api-key-here
   ```

4. **Run the brainstorm system**
   ```bash
   python claude_brainstorm.py
   ```

---

## 👥 Meet the Team

### 🐶 Lou the Assistant
**Primary Coordinator**
- Project coordination and organization
- Information retrieval
- Team facilitation
- Administrative support

### 🐱 Mia the Creative
**Creative Strategist**
- Innovative marketing ideas
- Brand development
- Creative brainstorming
- Visual and conceptual thinking

### 🤖 Codi the Coder
**Technical Implementation Specialist**
- Software development
- Code architecture
- Technical problem-solving
- Multiple programming languages

### 🦉 Rev the Reviewer
**Quality Assurance Specialist**
- Code review and analysis
- Content quality assessment
- Constructive feedback
- Process improvement

### 🐙 Otto the Optimizer
**Efficiency Specialist**
- Performance optimization
- Process streamlining
- Resource efficiency
- Workflow enhancement

### 🐹 Ham the Joker
**Creative Entertainer**
- Humor and comedic timing
- Team morale boosting
- Creative wordplay
- Observational comedy

### 🦊 Fin the Consultant
**Strategic Advisor**
- Strategic planning
- Project management
- Team coordination
- Long-term vision

### 🧚 Sam the Storyteller
**Narrative Architect**
- Storytelling and narratives
- World-building
- Character development
- Emotional engagement

### 🐿️ Doc the Documenter
**Knowledge Manager**
- Technical documentation
- Knowledge management
- Meeting summaries
- Information architecture

### 🐰 Van the Writer
**Content Creator**
- Copywriting and content
- Marketing materials
- Brand voice development
- Website copy

---

## 💡 Usage Examples

### Single-Agent Mode

Chat one-on-one with Lou for focused assistance:

```
👨‍💼 You: Help me plan a marketing campaign for our new product

🐶 Lou: I'd be happy to help you plan a marketing campaign! Let me organize
this into key areas...

[Lou provides structured guidance and support]
```

### Group Brainstorming Mode

Type `brainstorm` to activate all agents:

```
👨‍💼 You: brainstorm

✓ Switched to GROUP BRAINSTORM mode

👨‍💼 You (Group Mode): How can we make our app more engaging?

--- Round 1 ---

🐱 Mia the Creative:
Let me approach this with some creative thinking...
[Provides innovative engagement ideas]

🤖 Codi the Coder:
Building on Mia's suggestions, here's how we could implement...
[Proposes technical solutions]

🦉 Rev the Reviewer:
Great ideas from Mia and Codi. I'd add some considerations...
[Offers constructive feedback]

[... all 9 agents contribute in sequence ...]

==========================================================
END OF GROUP SESSION
==========================================================
```

---

## 🎯 Built-in Skills

### Ideation Skill
Generate creative ideas using proven techniques:
- SCAMPER method
- Mind mapping
- Six Thinking Hats

**Example:** "Use the ideation skill to brainstorm app features"

### Code Review Skill
Comprehensive code analysis covering:
- Functional correctness
- Security vulnerabilities
- Performance optimization
- Best practices

**Example:** "Review this authentication function for security issues"

### Storytelling Skill
Transform concepts into compelling narratives:
- Hero's Journey framework
- Problem-Solution-Impact structure
- Character-driven narratives

**Example:** "Turn our new feature into a customer success story"

---

## 🔧 Advanced Configuration

### Custom Agents

Create new agents in `.claude/agents/`:

```markdown
---
name: custom-agent
description: Your agent description
model: claude-sonnet-4-20250514
tools:
  - bash
  - file_operations
---

# Your Agent Name

Your agent's system prompt and instructions...
```

### Custom Skills

Add new skills in `.claude/skills/`:

```markdown
# Your Skill Name

Description of what this skill does...

## When to Use
...

## How It Works
...
```

### Custom Hooks

Create hooks in `.claude/hooks/`:

```python
def your_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Your hook description
    """
    # Your logic here
    return context
```

---

## 📊 Session Logging

All brainstorming sessions are automatically logged:

- **Location**: `./brainstorm_logs/`
- **Format**: Daily JSONL files
- **Summaries**: `./brainstorm_logs/summaries/`

Example log structure:
```json
{
  "timestamp": "2025-10-25T14:30:00",
  "user_message": "How can we improve user retention?",
  "agent_response": "...",
  "agent_name": "🐱 Mia the Creative",
  "mode": "group"
}
```

---

## 🆚 Comparison: Claude SDK vs Original AutoGen

| Feature | Original (AutoGen) | Claude SDK Version |
|---------|-------------------|-------------------|
| **LLM Provider** | Local Ollama models | Claude Sonnet 4.5 |
| **Agent Framework** | Microsoft AutoGen | Claude Agent SDK |
| **Subagents** | ❌ | ✅ |
| **Skills** | ❌ | ✅ (Built-in) |
| **Hooks** | ❌ | ✅ (Quality checks, logging) |
| **Async Support** | Limited | ✅ Full async |
| **Memory** | Teachability DB | Conversation context |
| **Session Logging** | Manual | ✅ Automatic |
| **API Costs** | Free (local) | Paid (Anthropic) |

---

## 🏗️ Architecture

```
claude_brainstorm.py          # Main application
├── BrainstormAgent          # Individual agent class
├── ClaudeBrainstormSystem   # Core system
│   ├── query_agent()        # Single agent queries
│   ├── group_brainstorm()   # Group sessions
│   └── interactive_session() # CLI interface
│
.claude/
├── agents/                  # Subagent configurations
│   ├── mia-creative.md
│   ├── codi-coder.md
│   └── ...
├── skills/                  # Reusable skills
│   ├── IDEATION.md
│   ├── CODE_REVIEW.md
│   └── STORYTELLING.md
└── hooks/                   # Automated workflows
    ├── brainstorm_logger.py
    └── quality_check.py
```

---

## 🤝 Contributing

We welcome contributions! Here are some ways to help:

- 🐛 Report bugs or issues
- 💡 Suggest new agent personalities
- 🎯 Create new skills
- 🔗 Develop useful hooks
- 📝 Improve documentation

---

## 📄 License

MIT License - Copyright 2024 2 Acre Studios

See [LICENSE.md](LICENSE.md) for details.

---

## 🔗 Resources

- [Claude Agent SDK Documentation](https://docs.claude.com/en/api/agent-sdk/overview)
- [Anthropic API Reference](https://docs.anthropic.com/)
- [Original AutoGen Version](groupchat_single_plus_brainstorm.py)
- [2 Acre Studios](https://2acrestudios.com)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/2acrestudios/autogen-brainstorm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/2acrestudios/autogen-brainstorm/discussions)
- **Website**: [2acrestudios.com](https://2acrestudios.com)

---

**Built with ❤️ by [2 Acre Studios](https://2acrestudios.com)**

*Empowering creative collaboration through AI*
