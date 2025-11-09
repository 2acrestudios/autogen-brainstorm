"""
Quality Check Hook

Validates responses before they are sent to ensure quality and appropriateness.
This hook is triggered before each response is sent to the user.
"""

from typing import Dict, Any, List
import re


def pre_response_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hook that performs quality checks on responses before sending.

    Args:
        context: The current context including the response to check

    Returns:
        Modified context with validated/enhanced response
    """
    response = context.get("response", "")

    # Check response length
    if len(response.strip()) < 10:
        context["warning"] = "Response too short - may need more context"

    # Check for code blocks (if agent is Codi)
    if context.get("agent_name", "").startswith("🤖 Codi"):
        if "```" not in response and any(keyword in response.lower() for keyword in ["function", "class", "def", "const", "let", "var"]):
            context["suggestion"] = "Consider wrapping code in markdown code blocks for better readability"

    # Check for collaborative references (addressing other agents)
    team_members = [
        "Mia", "Codi", "Rev", "Otto", "Ham", "Fin", "Sam", "Doc", "Van"
    ]

    if context.get("mode") == "group":
        has_reference = any(name in response for name in team_members)
        if not has_reference and len(context.get("contributions", [])) > 0:
            context["suggestion"] = "Consider referencing other team members' ideas for better collaboration"

    return context


def filter_duplicate_content(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hook that checks for and flags duplicate or repetitive content.

    Args:
        context: The current context

    Returns:
        Modified context
    """
    response = context.get("response", "")
    previous_responses = context.get("previous_responses", [])

    # Check for very similar responses (simple similarity check)
    for prev in previous_responses[-5:]:  # Check last 5 responses
        if prev and response:
            # Simple similarity: if more than 70% of words match
            current_words = set(response.lower().split())
            prev_words = set(prev.lower().split())

            if current_words and prev_words:
                similarity = len(current_words & prev_words) / max(len(current_words), len(prev_words))

                if similarity > 0.7:
                    context["warning"] = "Response may be too similar to previous content"
                    break

    return context
