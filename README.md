# Cupid Love

A small matchmaking [MCP](https://modelcontextprotocol.io) server built with [FastMCP](https://gofastmcp.com).
Create your profile, browse the fictional demo profiles in `data/profiles.json`, and get compatibility
scores, icebreakers and dating tips from any MCP client, such as Claude Desktop or Claude Code.

> Every candidate profile is **fictional**. Scores come from a simple, transparent algorithm and are estimates only.

## 1. Install uv

[uv](https://docs.astral.sh/uv/) manages Python, the virtual environment and dependencies for this project.

```bash
brew install uv
```

Or use the official installer (macOS / Linux):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check it works:

```bash
uv --version
```

## 2. Set up the project

From the project folder:

```bash
uv sync
```

This installs Python 3.14 if you don't have it (see `.python-version`), creates `.venv/`, and installs
`fastmcp` plus the project itself.

<details>
<summary>How this project was created (you don't need to run this)</summary>

```bash
uv init --package cupid-love
cd cupid-love
uv add fastmcp
```

`--package` creates the `src/cupid_love/` layout and the `cupid-love` command in `pyproject.toml`.
</details>

## 3. Start the server

```bash
uv run cupid-love
```

The server talks MCP over **stdio**, so after the FastMCP banner it just waits for a client. Stop it
with `Ctrl+C`. Normally you don't run it by hand: the MCP client starts it for you (see step 4).

To check that it works without a client, list its tools:

```bash
uv run fastmcp list --command "uv run cupid-love"
```

## 4. Connect it to a client

Replace `/ABSOLUTE/PATH/TO/cupid-love` with the full path to this folder (run `pwd` inside it).

### Claude Desktop

Open **Settings → Developer → Edit Config** and add:

```json
{
  "mcpServers": {
    "cupid-love": {
      "command": "uv",
      "args": ["--directory", "/ABSOLUTE/PATH/TO/cupid-love", "run", "cupid-love"]
    }
  }
}
```

Restart Claude Desktop. If it can't find `uv`, set `"command"` to the full path from `which uv`
(for example `/opt/homebrew/bin/uv`).

### Claude Code

```bash
claude mcp add cupid-love -- uv --directory /ABSOLUTE/PATH/TO/cupid-love run cupid-love
```

### MCP Inspector (optional, needs Node.js)

```bash
npx @modelcontextprotocol/inspector uv run cupid-love
```

## What the server offers

| Kind     | Name                      | What it does                                         |
| -------- | ------------------------- | ---------------------------------------------------- |
| Tool     | `get_daily_love_quote`    | A romantic quote for today                           |
| Tool     | `list_profiles`           | One-line summary of every (fictional) profile        |
| Tool     | `get_profile`             | Full profile by name, e.g. `Maya`                    |
| Tool     | `create_profile`          | Create and save your own profile (18+)               |
| Tool     | `get_my_profile`          | Show your saved profile and archetype                |
| Tool     | `update_personality`      | Change one personality trait (1–5)                   |
| Tool     | `calculate_compatibility` | Score 0–100 with you and someone, with reasons       |
| Tool     | `find_love_match`         | Your best matches, optionally filtered by interests  |
| Tool     | `generate_icebreaker`     | A respectful first message                           |
| Tool     | `get_love_advice`         | Tips for a topic such as `first_date`                |
| Resource | `cupid://profiles`        | All profiles as data                                 |
| Prompt   | `find_my_match`           | Starts a "find my match" conversation                |

Try asking your client: *"Create my Cupid profile, then find my best match and explain the score."*

## Data

- `data/profiles.json`: the fictional demo profiles.
- `data/me.json`: your profile, written by `create_profile`.

Set `CUPID_DATA_DIR` to keep the data somewhere else:

```bash
CUPID_DATA_DIR=/path/to/data uv run cupid-love
```

## Project layout

```
src/cupid_love/
├── __init__.py   # main(): entry point for `uv run cupid-love`
├── server.py     # FastMCP server: tools, resource and prompt
├── profiles.py   # load, search, create and save profiles
├── matching.py   # compatibility scoring
└── content.py    # quotes, icebreakers, advice, archetypes
```
