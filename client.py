"""Fixed-host OpenAI-compatible chat contract for dynamic Ace model IDs."""

from __future__ import annotations

import json
import os
import time
from typing import Any

import requests

API_BASE = "https://api.acedata.cloud/v1"


class AceChatError(RuntimeError):
    """A public error that never includes a raw response or API key."""


def credential() -> str:
    key = os.environ.get("ACEDATACLOUD_API_KEY") or os.environ.get("ACEDATACLOUD_API_TOKEN")
    if not key or not key.strip():
        raise AceChatError("Set ACEDATACLOUD_API_KEY in the ComfyUI process environment and restart.")
    key = key.strip()
    if key.lower().startswith("bearer "):
        key = key[7:].strip()
    if not key:
        raise AceChatError("Ace Data Cloud API key is empty.")
    return key


def _headers(key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {key}", "Accept": "application/json"}


def _http_error(status: int) -> AceChatError:
    if status in {401, 403}:
        return AceChatError(f"Ace Data Cloud returned HTTP {status}. Check key and model access.")
    if status == 404:
        return AceChatError("Model or chat endpoint not found. Check the exact model ID.")
    if status == 429:
        return AceChatError("Ace Data Cloud rate limit reached. Check request history before retrying.")
    return AceChatError(f"Ace Data Cloud returned HTTP {status}. Check request history before retrying.")


def list_models(filter_text: str = "") -> list[str]:
    key = credential()
    for attempt in range(3):
        try:
            response = requests.get(API_BASE + "/models", headers=_headers(key), timeout=(10, 30),
                                    allow_redirects=False)
            break
        except requests.RequestException as exc:
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise AceChatError(f"Model list connection failed ({type(exc).__name__}).") from None
    if response.status_code != 200:
        raise _http_error(response.status_code)
    try:
        body = response.json()
    except ValueError:
        raise AceChatError("Ace Data Cloud returned invalid model JSON.") from None
    if not isinstance(body, dict) or not isinstance(body.get("data"), list):
        raise AceChatError("Ace Data Cloud returned an unexpected model list.")
    models = sorted({item["id"] for item in body["data"] if isinstance(item, dict)
                     and isinstance(item.get("id"), str) and item["id"]})
    if filter_text:
        models = [model for model in models if filter_text.casefold() in model.casefold()]
    return models


def _messages(prompt: str, system_prompt: str, messages_json: str) -> list[dict[str, Any]]:
    if messages_json.strip():
        try:
            messages = json.loads(messages_json)
        except ValueError:
            raise ValueError("messages_json must be a JSON array of chat messages.") from None
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages_json must be a nonempty JSON array.")
    else:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("A prompt or messages_json is required.")
        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})
        messages.append({"role": "user", "content": prompt.strip()})
    allowed_roles = {"system", "developer", "user", "assistant", "tool"}
    if not all(isinstance(item, dict) and item.get("role") in allowed_roles and "content" in item
               for item in messages):
        raise ValueError("Each chat message needs a supported role and content.")
    return messages


def chat(model_id: str, prompt: str, system_prompt: str = "", messages_json: str = "",
         tools_json: str = "", temperature: float = -1, max_tokens: int = 1024) -> tuple[str, str, str, str, str]:
    if not isinstance(model_id, str) or not model_id.strip():
        raise ValueError("An exact Ace Data Cloud model ID is required.")
    if not isinstance(temperature, (int, float)) or temperature != -1 and not 0 <= temperature <= 2:
        raise ValueError("Temperature must be -1 (model default) or 0–2.")
    if not isinstance(max_tokens, int) or not 1 <= max_tokens <= 32768:
        raise ValueError("max_tokens must be 1–32768.")
    messages = _messages(prompt, system_prompt, messages_json)
    payload: dict[str, Any] = {"model": model_id.strip(), "messages": messages,
                               "max_tokens": max_tokens, "stream": False}
    if temperature != -1:
        payload["temperature"] = temperature
    if tools_json.strip():
        try:
            tools = json.loads(tools_json)
        except ValueError:
            raise ValueError("tools_json must be a JSON array.") from None
        if not isinstance(tools, list) or not tools:
            raise ValueError("tools_json must be a nonempty JSON array.")
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    key = credential()
    try:
        response = requests.post(API_BASE + "/chat/completions", json=payload,
                                 headers=_headers(key), timeout=(10, 120), allow_redirects=False)
    except requests.RequestException as exc:
        raise AceChatError(
            f"Chat submission connection failed ({type(exc).__name__}). "
            "Inspect request history before another paid request."
        ) from None
    if response.status_code != 200:
        raise _http_error(response.status_code)
    try:
        body = response.json()
    except ValueError:
        raise AceChatError("Ace Data Cloud returned invalid chat JSON.") from None
    if not isinstance(body, dict) or not isinstance(body.get("choices"), list) or not body["choices"]:
        raise AceChatError("Ace Data Cloud returned an unexpected chat response.")
    first = body["choices"][0]
    message = first.get("message") if isinstance(first, dict) else None
    if not isinstance(message, dict):
        raise AceChatError("Ace Data Cloud returned an invalid assistant message.")
    content = message.get("content")
    assistant_text = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False) if content is not None else ""
    tool_calls = message.get("tool_calls") or []
    if not isinstance(tool_calls, list):
        tool_calls = []
    usage = body.get("usage") or {}
    if not isinstance(usage, dict):
        usage = {}
    public_usage = {name: usage[name] for name in ("prompt_tokens", "completion_tokens", "total_tokens")
                    if name in usage}
    return (assistant_text, json.dumps(tool_calls, ensure_ascii=False),
            json.dumps(public_usage), str(body.get("id") or ""), str(body.get("model") or model_id.strip()))
