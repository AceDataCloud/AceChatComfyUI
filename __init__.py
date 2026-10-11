"""Ace Data Cloud dynamic chat nodes for ComfyUI."""

from .nodes import AceChatCompletion, AceChatListModels

NODE_CLASS_MAPPINGS = {
    "AceChatListModels": AceChatListModels,
    "AceChatCompletion": AceChatCompletion,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AceChatListModels": "Ace Chat List Models (Ace Data Cloud)",
    "AceChatCompletion": "Ace Chat Completion (Ace Data Cloud)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
