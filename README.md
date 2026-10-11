# Ace Chat for ComfyUI by Ace Data Cloud

Use a **dynamic model ID** with Ace Data Cloud's chat completions API from a ComfyUI graph. This package mirrors [ModelProviderDify](https://github.com/AceDataCloud/ModelProviderDify), whose model is configured by an exact ID rather than a finite selector. A read-only node lists the IDs currently returned for your Ace key. Chat completions may consume Credits at the [current model price](https://platform.acedata.cloud/models).

[简体中文](docs/README.zh-CN.md) · [Ace Data Cloud](https://platform.acedata.cloud) · [Issues](https://github.com/AceDataCloud/AceChatComfyUI/issues)

| Node | Purpose |
| --- | --- |
| **Ace Chat List Models** | Read `/v1/models` and optionally filter IDs; no chat generation |
| **Ace Chat Completion** | Send one non-streaming `/v1/chat/completions` request using an exact model ID |

The chat node returns assistant text, tool calls JSON, usage JSON, response ID, and response model as standard ComfyUI strings. `model_id` is free text so newly available IDs are not blocked by a stale package enum. The model list can include IDs that use another API surface; choose a chat-compatible ID and check its current access and price. The node returns function tool calls but does not execute those functions.

## Install

When the Registry version is active, open **ComfyUI-Manager → Custom Nodes**, search **Ace Chat**, confirm publisher **acedatacloud** and package **Ace Chat by Ace Data Cloud**, install, and restart. Registry ID: `ace-chat`; source: `AceDataCloud/AceChatComfyUI`. Source availability or Registry upload alone does not prove Manager installation.

For local source testing:

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/AceDataCloud/AceChatComfyUI.git
cd AceChatComfyUI
python -m pip install -r requirements.txt
```

Restart ComfyUI and search for **Ace Chat**.

## Set your key

Set an Ace key with chat access in the **actual ComfyUI process environment**, then restart:

```bash
export ACEDATACLOUD_API_KEY='paste-your-key-here'
python main.py --cpu
```

`ACEDATACLOUD_API_TOKEN` is also accepted. Keep the key out of workflows, screenshots, issues, and the repository. If you restrict API paths, allow `/v1/models` and `/v1/chat/completions`.

## Choose a model and chat

Import [01-list-models.json](examples/01-list-models.json) with **File → Open** and run it. This is a read-only request. Copy an exact chat-compatible ID into **Ace Chat Completion**. The Dify provider uses the same fixed `/v1` endpoint and a customizable model ID; this ComfyUI node follows that contract. The model list can change without a package release.

Import [02-chat-completion.json](examples/02-chat-completion.json), check the selected model's price, and run **once**. The example is a paid-call template. `prompt` plus optional `system_prompt` creates a simple conversation. `messages_json` can instead contain a full nonempty JSON message array; when present it takes precedence over those two fields. `tools_json` can provide an OpenAI-compatible function tool array. A temperature of `-1` omits the parameter and uses the model default; `max_tokens` limits output.

If the paid request times out, inspect Ace request history before another run. The node does not automatically retry chat submissions. To inspect current usage, use the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications). See [privacy notes](docs/PRIVACY.md).

## Development

```bash
python -m unittest discover -s tests -v
python -m py_compile __init__.py client.py nodes.py
```

`pyproject.toml` declares Registry ID `ace-chat`, publisher `acedatacloud`, and a 400×400 proportional resize of the [canonical Ace logo](https://cdn.acedata.cloud/assets/logo.png).
