"""Check that the skill is complete and references exist."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class IntegrityTests(unittest.TestCase):
    def test_entrypoint_and_agent(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: prawnik-pl\n"))
        self.assertIn("description:", content)
        self.assertTrue((ROOT / "agents" / "openai.yaml").is_file())

    def test_all_markdown_local_links(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for relative in re.findall(r"\]\((references/[^)]+|assets/[^)]+)\)", text):
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_areas_count(self):
        self.assertEqual(len(list((ROOT / "references").glob("area-*.md"))), 13)

    def test_no_todo_placeholders(self):
        for file in ROOT.rglob("*.md"):
            text = file.read_text(encoding="utf-8")
            self.assertNotIn("[TODO:", text, str(file))

    def test_script_has_no_network_imports(self):
        text = (ROOT / "scripts" / "legal_calc.py").read_text(encoding="utf-8")
        self.assertNotIn("import requests", text)
        self.assertNotIn("urllib.request", text)


if __name__ == "__main__":
    unittest.main()
