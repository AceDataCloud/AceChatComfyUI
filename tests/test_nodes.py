"""ComfyUI node registration and text output shape."""

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ace_chat_comfy", ROOT / "__init__.py", submodule_search_locations=[str(ROOT)]
)
package = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = package
spec.loader.exec_module(package)
nodes = sys.modules["ace_chat_comfy.nodes"]


class AceChatNodeTests(unittest.TestCase):
    def test_model_id_is_freeform_not_a_stale_enum(self):
        model_input = nodes.AceChatCompletion.INPUT_TYPES()["required"]["model_id"]
        self.assertEqual(model_input[0], "STRING")
        self.assertIn("AceChatListModels", package.NODE_CLASS_MAPPINGS)

    def test_chat_result_is_visible_as_comfy_string(self):
        with patch.object(nodes, "chat", return_value=("Hello", "[]", "{}", "chat-123", "gpt-4.1-mini")):
            value = nodes.AceChatCompletion().run("gpt-4.1-mini", "Hi", "", "", "", -1, 1024)
        self.assertEqual(value["result"][0], "Hello")
        self.assertIn("chat-123", " ".join(value["ui"]["text"]))


if __name__ == "__main__":
    unittest.main()
