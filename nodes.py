"""ComfyUI STRING nodes for dynamic Ace chat model IDs."""

from __future__ import annotations

import json

from .client import chat, list_models


class AceChatListModels:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"filter_text": ("STRING", {"default": ""})}}

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("model_ids_json", "count")
    FUNCTION = "run"
    CATEGORY = "Ace Data Cloud/Chat"
    DESCRIPTION = "Read currently available model IDs from the Ace API without a paid chat request."
    OUTPUT_NODE = True

    def run(self, filter_text: str):
        models = list_models(filter_text)
        return {"ui": {"text": [f"Ace chat model IDs: {len(models)}",
                                "Copy an exact chat-compatible ID into Chat Completion."]},
                "result": (json.dumps(models), len(models))}


class AceChatCompletion:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "model_id": ("STRING", {"default": "gpt-4.1-mini"}),
            "prompt": ("STRING", {"multiline": True, "default": "Explain this workflow in one sentence."}),
            "system_prompt": ("STRING", {"multiline": True, "default": ""}),
            "messages_json": ("STRING", {"multiline": True, "default": ""}),
            "tools_json": ("STRING", {"multiline": True, "default": ""}),
            "temperature": ("FLOAT", {"default": -1, "min": -1, "max": 2, "step": 0.05}),
            "max_tokens": ("INT", {"default": 1024, "min": 1, "max": 32768}),
        }}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("assistant_text", "tool_calls_json", "usage_json", "response_id", "response_model")
    FUNCTION = "run"
    CATEGORY = "Ace Data Cloud/Chat"
    DESCRIPTION = "Send one paid, non-streaming chat completion to an exact Ace model ID."
    OUTPUT_NODE = True

    def run(self, model_id, prompt, system_prompt, messages_json, tools_json, temperature, max_tokens):
        result = chat(model_id, prompt, system_prompt, messages_json, tools_json, temperature, max_tokens)
        return {"ui": {"text": [f"Ace chat model: {result[4]}",
                                f"Response ID: {result[3] or 'unavailable'}",
                                result[0] or "Assistant returned tool calls or empty text."]},
                "result": result}
