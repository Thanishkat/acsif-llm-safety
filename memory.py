# core/memory.py

from typing import Dict, List


class MemoryManager:
    """
    Lightweight in-session memory.
    This does not persist private data to disk.
    """

    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def add(self, user_message: str, assistant_message: str) -> None:
        self.history.append({
            "user": user_message,
            "assistant": assistant_message,
        })

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def clear(self) -> None:
        self.history.clear()
