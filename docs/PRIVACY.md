# Privacy

- List Models sends the Ace key to `https://api.acedata.cloud/v1/models` and returns model IDs; it does not generate chat output.
- Chat Completion sends the selected model ID, prompts or message array, optional tool definitions, and the process environment's Ace key to `https://api.acedata.cloud/v1/chat/completions`.
- The package does not save keys in workflows or logs. ComfyUI's own workflow/history may retain non-secret inputs and model outputs.
- Chat submissions may consume Credits and are never automatically retried after a connection failure.
