"""Unit tests for the Markdown link checker."""

import tempfile
import unittest
from pathlib import Path

from check_markdown_links import extract_links, local_target_exists


class MarkdownLinkCheckerTests(unittest.TestCase):
    def test_extracts_links_and_images_but_skips_code(self):
        markdown = """[valid](docs/page.md)
![image](images/example.png)
`[inline](missing-inline.md)`
```markdown
[inside-fence](missing-fence.md)
```
[external](https://example.com/page)
"""
        found = list(extract_links(markdown))
        self.assertEqual(
            found,
            [
                (1, "docs/page.md"),
                (2, "images/example.png"),
                (7, "https://example.com/page"),
            ],
        )

    def test_resolves_relative_and_percent_encoded_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "knowledge" / "topic.md"
            target = root / "knowledge" / "support file.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Topic", encoding="utf-8")
            target.write_text("# Support", encoding="utf-8")

            self.assertTrue(local_target_exists(root, source, "support%20file.md"))

    def test_accepts_directory_with_index_or_readme(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "topic.md"
            folder = root / "reference"
            folder.mkdir()
            (folder / "index.md").write_text("# Index", encoding="utf-8")
            source.write_text("# Topic", encoding="utf-8")

            self.assertTrue(local_target_exists(root, source, "reference/"))

    def test_external_and_fragment_links_are_not_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "topic.md"
            source.write_text("# Topic", encoding="utf-8")

            self.assertTrue(local_target_exists(root, source, "https://example.com"))
            self.assertTrue(local_target_exists(root, source, "#section"))

    def test_missing_and_out_of_repo_targets_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            source = root / "topic.md"
            source.write_text("# Topic", encoding="utf-8")

            self.assertFalse(local_target_exists(root, source, "missing.md"))
            self.assertFalse(local_target_exists(root, source, "../outside.md"))


if __name__ == "__main__":
    unittest.main()
