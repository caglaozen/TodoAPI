"""
ADK Entry Point - Alternative Path.
ADK bazen src.agent.root_agent path'ini de arar.
"""

from .todo_agent import todo_agent

# ADK convention: root_agent adında bir değişken gerekli.
root_agent = todo_agent

print("✅ Alternative ADK Root Agent entry point oluşturuldu!") 