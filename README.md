# arxiv-digest

A Claude Code plugin that turns the day's arXiv announcements into a digest ranked against **your** research profile.

It fetches every new submission, cross-list and replacement for the arXiv subjects you follow, triages each one into Tier A (core), Tier B (adjacent) or Tier C (everything else) from title and abstract, reads the most relevant papers in depth, and writes one Markdown digest per announcement day. Optionally it also builds a phone-friendly web page and sends a push notification.

## Install

In Claude Code:

```
/plugin marketplace add Moral-eddy/arxiv-digest
/plugin install arxiv-digest@arxiv-digest
```

Requirements: Python 3 (standard library only) and [`uv`](https://docs.astral.sh/uv/) (the plugin starts the [arXiv MCP server](https://github.com/blazickjp/arxiv-mcp-server) through `uvx` for close readings; without it the skill falls back to the arXiv HTML pages).

## Use

Open a folder you want the digests to live in and ask Claude:

> Run my arXiv digest

or invoke the skill directly with `/arxiv-digest:arxiv-digest`. The first run interviews you about your subjects, research focus and anchor papers, writes `.arxiv-digest/config.json`, and then produces the first digest in `arxiv-digests/`.

## Make it yours

Nothing about the focus is built in; it all comes from your profile in `.arxiv-digest/config.json`:

- **Your words:** describe what you work on, or give a few of your own papers and let Claude infer it. Tier A is "drop everything", Tier B is "worth a look".
- **Several focus areas,** each with its own Tier A and B description, and the digest names the one a paper matched.
- **Anchor papers,** so Tier A entries say how they relate to the work you build on.
- **Followed authors** (always at least Tier B) and **muted kinds** of paper (kept in Tier C).
- **Calibration examples:** say "that paper should have been Tier A, because..." after a digest and the profile is tuned; the judgment is kept as an example so the next triage follows it.
- **Subjects, language, how many close readings,** and whether cross-lists and replacements are shown.

You can send your `config.json` to a colleague as a starting point for theirs.

Later:

- "Change my arXiv profile" or "tune my arXiv focus" edits the config.
- "Schedule my arXiv digest" walks through [scheduling](skills/arxiv-digest/references/scheduling.md): arXiv publishes in the evening US Eastern time, so a few triggers through the night catch the batch whenever the feed updates, and extra runs do nothing.

## What is in the box

| Path | Purpose |
|---|---|
| `skills/arxiv-digest/SKILL.md` | the procedure: fetch, check, triage, close-read, write, publish, notify |
| `skills/arxiv-digest/references/` | digest format contract, config schema, setup interview, scheduling, notifications |
| `skills/arxiv-digest/scripts/` | `fetch_arxiv.py` (RSS fetch) and `build_site.py` (phone page) |
| `skills/arxiv-digest/assets/site-template.html` | the page template |
| `.mcp.json` | the arXiv MCP server, pinned, storing papers under the plugin's data folder |

## Privacy and security

- Your profile, digests and notification settings stay in your working directory (`.arxiv-digest/`, `arxiv-digests/`). Nothing is sent anywhere except requests to arXiv and, if you turn it on, the ntfy server and Claude's Artifact publishing.
- The ntfy topic is stored in its own file, not in the config, because on the public ntfy.sh server the topic name works like a password.
- The phone page loads marked, DOMPurify and MathJax from cdnjs and fonts from Google Fonts in the viewer's browser.
- Paper text is treated as data, never as instructions.

## Using only the skill

Copy `skills/arxiv-digest/` into `~/.claude/skills/` (or a project's `.claude/skills/`). The skill then works without the plugin wrapper, but you lose the bundled MCP server config (the skill falls back to arXiv HTML pages) and the `${CLAUDE_PLUGIN_ROOT}` paths in `SKILL.md` and the references need to point at the copied folder.

## Licence and credits

MIT, see [LICENSE](LICENSE). Written by Moral E. together with Claude (Anthropic). The RSS fetch script and the arXiv category list are from [yang3kc/daily_arxiv_digest](https://github.com/yang3kc/daily_arxiv_digest) (MIT); see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
