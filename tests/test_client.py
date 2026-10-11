"""Dynamic model discovery and paid chat boundary."""

import os
import unittest
from unittest.mock import Mock, patch

import client


class AceChatClientTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {"ACEDATACLOUD_API_KEY": "test-key"})
        env.start()
        self.addCleanup(env.stop)

    @patch("client.requests.get")
    def test_model_list_is_read_only_and_dynamic(self, get):
        get.return_value = Mock(status_code=200)
        get.return_value.json.return_value = {"data": [
            {"id": "gpt-4.1-mini"}, {"id": "grok-4"}, {"id": "gpt-4.1-mini"}]}
        self.assertEqual(client.list_models("gpt"), ["gpt-4.1-mini"])
        get.assert_called_once()
        self.assertEqual(get.call_args.args[0], "https://api.acedata.cloud/v1/models")
        self.assertFalse(get.call_args.kwargs["allow_redirects"])

    @patch("client.requests.post")
    def test_chat_uses_exact_model_id_and_returns_public_outputs(self, post):
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {
            "id": "chat-123", "model": "gpt-4.1-mini",
            "choices": [{"message": {"role": "assistant", "content": "Hello"}}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5,
                      "internal_price": 99},
        }
        result = client.chat("gpt-4.1-mini", "Hi", "Be concise")
        self.assertEqual(result, ("Hello", "[]", '{"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5}',
                                  "chat-123", "gpt-4.1-mini"))
        post.assert_called_once()
        self.assertEqual(post.call_args.args[0], "https://api.acedata.cloud/v1/chat/completions")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["messages"], [{"role": "system", "content": "Be concise"},
                                               {"role": "user", "content": "Hi"}])
        self.assertFalse(payload["stream"])

    @patch("client.requests.post")
    def test_paid_chat_timeout_never_retries_or_leaks_key(self, post):
        post.side_effect = client.requests.Timeout("Bearer test-key")
        with self.assertRaises(client.AceChatError) as caught:
            client.chat("gpt-4.1-mini", "Hi")
        post.assert_called_once()
        self.assertNotIn("test-key", str(caught.exception))

    @patch("client.requests.post")
    def test_invalid_messages_stop_before_payment(self, post):
        with self.assertRaises(ValueError):
            client.chat("gpt-4.1-mini", "", messages_json='{"not":"array"}')
        with self.assertRaises(ValueError):
            client.chat("", "Hi")
        post.assert_not_called()

    @patch("client.requests.post")
    def test_tool_calls_remain_json_for_downstream_nodes(self, post):
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {
            "choices": [{"message": {"role": "assistant", "content": None,
                "tool_calls": [{"id": "call-1", "type": "function", "function": {"name": "lookup", "arguments": "{}"}}]}}]
        }
        result = client.chat("grok-4", "Find a fact", tools_json='[{"type":"function","function":{"name":"lookup","parameters":{"type":"object"}}}]')
        self.assertEqual(result[0], "")
        self.assertIn('"call-1"', result[1])
        self.assertEqual(post.call_args.kwargs["json"]["tool_choice"], "auto")


if __name__ == "__main__":
    unittest.main()
