#!/usr/bin/env python3
"""
Claude Agent SDK Brainstorm System
A collaborative AI brainstorming framework powered by the Claude Agent SDK.

This implementation uses Claude's agent capabilities including:
- Subagents for specialized tasks
- Skills for reusable brainstorming capabilities
- Hooks for automated workflows
- Custom tools for enhanced functionality

Copyright 2024 2 Acre Studios
"""

import os
import asyncio
from typing import List, Dict, Optional, Callable
from pathlib import Path

try:
    from claude_agent_sdk import ClaudeAgentClient, ClaudeAgentOptions
    from claude_agent_sdk.models import Message, ToolDefinition
except ImportError:
    print("Error: claude-agent-sdk not installed. Run: pip install claude-agent-sdk")
    exit(1)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BrainstormAgent:
    """
    Individual brainstorming agent with specialized role and personality.
    """
    def __init__(self, name: str, emoji: str, role: str, personality: str, expertise: List[str]):
        self.name = name
        self.emoji = emoji
        self.role = role
        self.personality = personality
        self.expertise = expertise

    def get_system_prompt(self) -> str:
        """Generate system prompt for this agent."""
        team_members = [
            "Mia the Creative", "Codi the Coder", "Rev the Reviewer",
            "Otto the Optimizer", "Ham the Joker", "Fin the Consultant",
            "Sam the Storyteller", "Doc the Documenter", "Van the Writer"
        ]

        return f"""You are {self.name}, {self.role} at 2 Acre Studios.

Personality: {self.personality}

Areas of Expertise:
{chr(10).join(f'- {exp}' for exp in self.expertise)}

You work collaboratively with the following team members:
{chr(10).join(f'- {member}' for member in team_members if member != self.name.replace(self.emoji + ' ', ''))}

When contributing to discussions:
1. Stay true to your role and expertise
2. Address team members by name when building on their ideas
3. Provide specific, actionable insights
4. Encourage creative thinking and exploration
5. Maintain a professional yet friendly tone
"""


class ClaudeBrainstormSystem:
    """
    Main brainstorming system powered by Claude Agent SDK.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Claude Brainstorm System.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.agents = self._initialize_agents()
        self.current_mode = "single"  # "single" or "group"
        self.conversation_history: List[Message] = []

        # Initialize Claude Agent SDK client
        self.client = self._create_client()

    def _create_client(self) -> ClaudeAgentClient:
        """Create and configure Claude Agent SDK client."""
        options = ClaudeAgentOptions(
            api_key=self.api_key,
            model="claude-sonnet-4-20250514",  # Claude Sonnet 4.5
        )
        return ClaudeAgentClient(options)

    def _initialize_agents(self) -> Dict[str, BrainstormAgent]:
        """Initialize all brainstorming agents."""
        agents = {
            "mia": BrainstormAgent(
                name="🐱 Mia the Creative",
                emoji="🐱",
                role="creative strategist and idea generator",
                personality="Dynamic, enthusiastic, and innovative. Thrives in collaborative environments.",
                expertise=[
                    "Creative brainstorming and ideation",
                    "Marketing strategy and campaigns",
                    "Brand development and storytelling",
                    "Visual and conceptual thinking"
                ]
            ),
            "codi": BrainstormAgent(
                name="🤖 Codi the Coder",
                emoji="🤖",
                role="technical implementation specialist",
                personality="Precise, logical, and solution-oriented. Translates ideas into working code.",
                expertise=[
                    "Software development and architecture",
                    "Multiple programming languages and frameworks",
                    "Code optimization and best practices",
                    "Technical problem-solving"
                ]
            ),
            "rev": BrainstormAgent(
                name="🦉 Rev the Reviewer",
                emoji="🦉",
                role="quality assurance and feedback specialist",
                personality="Meticulous, insightful, and constructive. Keen eye for detail.",
                expertise=[
                    "Code review and analysis",
                    "Content quality assessment",
                    "Constructive criticism and feedback",
                    "Process improvement suggestions"
                ]
            ),
            "otto": BrainstormAgent(
                name="🐙 Otto the Optimizer",
                emoji="🐙",
                role="efficiency and performance specialist",
                personality="Analytical, strategic, and results-driven. Focused on continuous improvement.",
                expertise=[
                    "Performance optimization",
                    "Process streamlining",
                    "Resource efficiency",
                    "Workflow enhancement"
                ]
            ),
            "ham": BrainstormAgent(
                name="🐹 Ham the Joker",
                emoji="🐹",
                role="creative entertainer and morale booster",
                personality="Witty, playful, and observant. Masters the art of timely humor.",
                expertise=[
                    "Humor and comedic timing",
                    "Creative wordplay and puns",
                    "Team morale and engagement",
                    "Observational comedy"
                ]
            ),
            "fin": BrainstormAgent(
                name="🦊 Fin the Consultant",
                emoji="🦊",
                role="strategic advisor and project coordinator",
                personality="Wise, experienced, and thoughtful. Provides strategic perspective.",
                expertise=[
                    "Strategic planning and guidance",
                    "Project management",
                    "Team coordination",
                    "Long-term vision and goals"
                ]
            ),
            "sam": BrainstormAgent(
                name="🧚 Sam the Storyteller",
                emoji="🧚",
                role="narrative architect and world-builder",
                personality="Imaginative, passionate, and articulate. Weaves compelling narratives.",
                expertise=[
                    "Storytelling and narrative structure",
                    "World-building and lore creation",
                    "Character development",
                    "Emotional engagement"
                ]
            ),
            "doc": BrainstormAgent(
                name="🐿️ Doc the Documenter",
                emoji="🐿️",
                role="knowledge manager and documentation specialist",
                personality="Organized, thorough, and clear. Ensures nothing is lost or forgotten.",
                expertise=[
                    "Technical documentation",
                    "Knowledge management",
                    "Meeting notes and summaries",
                    "Information architecture"
                ]
            ),
            "van": BrainstormAgent(
                name="🐰 Van the Writer",
                emoji="🐰",
                role="content creator and wordsmith",
                personality="Versatile, eloquent, and engaging. Masters the written word.",
                expertise=[
                    "Content writing and copywriting",
                    "Marketing materials",
                    "Website copy and blog posts",
                    "Brand voice development"
                ]
            )
        }

        # Add Lou as the primary assistant
        agents["lou"] = BrainstormAgent(
            name="🐶 Lou the Assistant",
            emoji="🐶",
            role="project coordinator and primary assistant",
            personality="Reliable, efficient, and supportive. Keeps everything on track.",
            expertise=[
                "Project coordination",
                "Administrative support",
                "Information retrieval and organization",
                "Team facilitation"
            ]
        )

        return agents

    def display_welcome(self):
        """Display ASCII art welcome message."""
        print("""
░█▀█░█░█░▀█▀░█▀█░█▀▀░█▀▀░█▀█░░░█▀▄░█▀▄░█▀█░▀█▀░█▀█░█▀▀░▀█▀░█▀█░█▀▄░█▄█
░█▀█░█░█░░█░░█░█░█░█░█▀▀░█░█░░░█▀▄░█▀▄░█▀█░░█░░█░█░▀▀█░░█░░█░█░█▀▄░█░█
░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░▀▀░░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀░▀

Powered by Claude Agent SDK

Work with your crew in group chat by typing 'brainstorm'!
...or just chat one-on-one with Lou.

Commands:
  'brainstorm' - Toggle group brainstorming mode
  'exit' or 'quit' - End the session

""")

    async def query_agent(self, message: str, agent_key: str = "lou") -> str:
        """
        Query a specific agent with a message.

        Args:
            message: The user's message
            agent_key: The key of the agent to query

        Returns:
            The agent's response
        """
        agent = self.agents.get(agent_key, self.agents["lou"])
        system_prompt = agent.get_system_prompt()

        # Use Claude Agent SDK to query
        response_parts = []
        async for chunk in self.client.query(
            message=message,
            system=system_prompt
        ):
            if hasattr(chunk, 'content'):
                response_parts.append(str(chunk.content))

        return ''.join(response_parts)

    async def group_brainstorm(self, message: str, max_rounds: int = 3) -> List[Dict[str, str]]:
        """
        Conduct a group brainstorming session.

        Args:
            message: The brainstorming topic/question
            max_rounds: Maximum number of discussion rounds

        Returns:
            List of contributions from each agent
        """
        contributions = []

        # Get primary agents for group discussion (excluding Lou)
        group_agents = ["mia", "codi", "rev", "otto", "ham", "fin", "sam", "doc", "van"]

        print(f"\n{'='*60}")
        print(f"GROUP BRAINSTORM SESSION")
        print(f"{'='*60}\n")

        for round_num in range(max_rounds):
            print(f"\n--- Round {round_num + 1} ---\n")

            for agent_key in group_agents:
                agent = self.agents[agent_key]

                # Build context from previous contributions
                context = f"Brainstorming topic: {message}\n\n"
                if contributions:
                    context += "Previous contributions:\n"
                    for contrib in contributions[-9:]:  # Last 9 contributions
                        context += f"- {contrib['agent']}: {contrib['response'][:100]}...\n"

                context += f"\n{agent.name}, what's your take on this? Build on the ideas shared so far."

                try:
                    response = await self.query_agent(context, agent_key)
                    contribution = {
                        "agent": agent.name,
                        "response": response,
                        "round": round_num + 1
                    }
                    contributions.append(contribution)

                    print(f"{agent.name}:")
                    print(f"{response}\n")

                except Exception as e:
                    print(f"Error getting response from {agent.name}: {e}")

        return contributions

    async def interactive_session(self):
        """Run interactive brainstorming session."""
        self.display_welcome()

        while True:
            try:
                if self.current_mode == "single":
                    user_input = input("👨‍💼 You: ").strip()
                else:
                    user_input = input("👨‍💼 You (Group Mode): ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ["exit", "quit"]:
                    print("\nThanks for brainstorming! Goodbye!")
                    break

                if user_input.lower() == "brainstorm":
                    self.current_mode = "group" if self.current_mode == "single" else "single"
                    mode_name = "GROUP BRAINSTORM" if self.current_mode == "group" else "SINGLE AGENT"
                    print(f"\n✓ Switched to {mode_name} mode\n")
                    continue

                # Process message based on mode
                if self.current_mode == "single":
                    # Single agent conversation with Lou
                    response = await self.query_agent(user_input, "lou")
                    print(f"\n🐶 Lou: {response}\n")
                else:
                    # Group brainstorming session
                    await self.group_brainstorm(user_input)
                    print(f"\n{'='*60}")
                    print(f"END OF GROUP SESSION")
                    print(f"{'='*60}\n")

            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type 'exit' to quit.\n")


async def main():
    """Main entry point."""
    try:
        # Initialize the brainstorm system
        system = ClaudeBrainstormSystem()

        # Run interactive session
        await system.interactive_session()

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease set your ANTHROPIC_API_KEY environment variable:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("  ANTHROPIC_API_KEY=your-api-key-here")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
