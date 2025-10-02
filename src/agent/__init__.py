"""
Todo Agent module.
AI agent for managing todo items using Google ADK.
"""

from .todo_agent import todo_agent

# ADK requires a root_agent to be exposed
root_agent = todo_agent

__all__ = ['root_agent', 'todo_agent'] 