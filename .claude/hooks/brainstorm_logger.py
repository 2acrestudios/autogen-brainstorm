"""
Brainstorm Logger Hook

Automatically logs all brainstorming sessions to a file for later review.
This hook is triggered after each agent response.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def after_response_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hook that logs brainstorming sessions after each response.

    Args:
        context: The current context including message, response, and metadata

    Returns:
        Modified context (or unchanged)
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("./brainstorm_logs")
    log_dir.mkdir(exist_ok=True)

    # Create log entry
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "user_message": context.get("message", ""),
        "agent_response": context.get("response", ""),
        "agent_name": context.get("agent_name", "unknown"),
        "mode": context.get("mode", "single")
    }

    # Append to daily log file
    log_file = log_dir / f"brainstorm_{datetime.now().strftime('%Y-%m-%d')}.jsonl"

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return context


def session_summary_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hook that generates a summary at the end of group brainstorming sessions.

    Args:
        context: The current context

    Returns:
        Modified context with summary
    """
    if context.get("mode") == "group" and context.get("session_ending", False):
        contributions = context.get("contributions", [])

        if contributions:
            summary = {
                "session_date": datetime.now().isoformat(),
                "topic": context.get("topic", ""),
                "total_contributions": len(contributions),
                "agents_participated": len(set(c.get("agent", "") for c in contributions)),
                "key_insights": []
            }

            # Save summary
            summary_dir = Path("./brainstorm_logs/summaries")
            summary_dir.mkdir(parents=True, exist_ok=True)

            summary_file = summary_dir / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(summary_file, "w") as f:
                json.dump(summary, f, indent=2)

            print(f"\n✓ Session summary saved to {summary_file}")

    return context
