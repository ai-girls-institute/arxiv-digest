# Phone page and notifications (optional)

Both are best effort. A failure never invalidates the digest; note it in the report and continue.

## Phone page

Build `<digest dir>/site/index.html` from every digest (newest first). The result is one self-contained HTML file with the digests embedded:

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/skills/arxiv-digest/scripts/build_site.py" --digests-dir "<digest dir>" --prefix "<prefix>" --title "<site.title>" --kicker "<site.kicker>"
```

(`--title` and `--kicker` are optional; they default from the prefix.)

Publish it with the Artifact tool, if your session has one:

1. Read the existing artifact at `site.artifact_url` (action `read`).
2. Publish `<digest dir>/site/index.html` with `url` set to `site.artifact_url`. No icon, no new title; keep it private; no capabilities.
3. If the publish is refused because a newer version exists, read the saved copy it points to, check that every digest embedded in it also exists in your build (rebuild if not), then publish again.
4. If the Artifact tool is unavailable or the publish needs an approval nobody can give, skip it and say so in the report.

The first publish, which creates the artifact and gives the URL to store in `site.artifact_url`, happens during setup with the user present. Do not create new artifacts in unattended runs.

Without the Artifact tool the file still works: open `index.html` locally, or copy it to any static host.

## Notification line

Only in a run that wrote a new digest. Never for "already digested" or "not yet published". Compose one plain line under 160 characters, no markdown, no quotes or backslashes, saying the digest is ready and leading with what matters:

- `ml Thu 8 Oct ready: 3 Tier A, 1 Tier B. Top: 2610.09238 Benchmark for long-context retrieval`
- `ml Fri 9 Oct ready: no Tier A/B today, 24 new`

If the page publish failed, end with `(page not updated)`.

## Phone, via ntfy

[ntfy](https://ntfy.sh) sends a push notification to a topic the phone subscribes to. On the public server the topic name is the only secret: anyone who knows it can read and write it. So:

- Read the topic from `notify.ntfy_topic_file` and the tap target from `notify.ntfy_click_file`. Do not print either into chat, logs, the digest or the config, and never edit them.
- Send to exactly that topic and nowhere else. Never put anything sensitive in the line.

```sh
curl -s -o /dev/null -w "%{http_code}" -H "Title: arXiv digest" -H "Click: <click url>" -H "Tags: books" -d "<the line>" "https://ntfy.sh/<topic>"
```

A 200 response means ntfy accepted it. Omit the `Click` header if `ntfy_click_file` is unset. To get the topic onto the phone, install the ntfy app and subscribe to the same topic name (the user picks a long random string).

## Mac banner (macOS only)

If `notify.mac_banner` is true:

```sh
osascript -e 'display notification "<the line>" with title "arXiv digest" sound name "Glass"'
```
