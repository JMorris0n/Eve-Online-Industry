# Repository validation tools

These scripts use Python's standard library and can be run locally from the repository root.

## Check internal Markdown links

PowerShell:

```powershell
py -3 tools/validation/check_markdown_links.py
```

The checker scans repository Markdown files and validates inline local file links and image targets. It skips generated exports, local data directories, external URLs, fragment-only links, fenced code blocks, and inline code.

Known limitations:
- It does not verify external URLs.
- It does not verify that heading fragments exist.
- It does not currently parse reference-style Markdown links or raw HTML links.
- Directory links require an `index.md` or `README.md` file.

## Test the validation tools

```powershell
py -3 -m unittest discover -s tools/validation -p "test_*.py" -v
```

## Full local quality check

From the repository root, run the complete local validation suite with one command:

```powershell
py -3 tools/validation/run_all.py
```

This executes calculation, repository-validation, operating-profile, SDE recipe-parser unit tests, and the Markdown link scan in sequence. It returns a non-zero exit code if any check group fails.

To run individual stages, use:

```powershell
py -3 -m unittest discover -s tools/calculations -p "test_*.py" -v
py -3 -m unittest discover -s tools/validation -p "test_*.py" -v
py -3 -m unittest discover -s tools/profile -p "test_*.py" -v
py -3 -m unittest discover -s tools/sde -p "test_*.py" -v
py -3 tools/validation/check_markdown_links.py
```

GitHub Actions runs the same checks for relevant code and documentation changes. A passing local-link check does not establish that external sources are reachable or that cited EVE mechanics are current.
