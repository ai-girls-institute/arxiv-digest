# Scheduling the digest

The digest is meant to run itself each announcement day. The skill is already idempotent, so a schedule can simply fire several times and let the extra runs do nothing.

## When arXiv publishes

arXiv announces Sunday to Thursday at 20:00 America/New_York ([availability](https://info.arxiv.org/help/availability.html)). The public RSS feed and `/list/<subject>/new` page have been observed to update later than that, around 00:00 America/New_York, so an early trigger often still sees the previous batch. That is expected: steps 2-3 of the skill detect it and exit without writing anything. Treat these times as observed, not guaranteed.

Recipe: one trigger every two hours, from just after 20:00 America/New_York until about 02:00 America/New_York, which runs well past the observed update time. Schedule it for Monday to Friday in your local time, because the announcement lands on the next calendar day in Europe and Asia. Example for central Europe in autumn (six hours ahead of New York): 02:05, 04:05, 06:05, 08:05. The offset to New York shifts by an hour for a week or two around each clock change, so recheck the times then. Never create retry tasks; the schedule is the retry.

## Prompt for the scheduled run

Use this as the task prompt; fill in the working directory where `.arxiv-digest/config.json` lives:

```
Run the arxiv-digest skill unattended in <WORKING DIRECTORY>. Use the existing profile in .arxiv-digest/config.json. Do not ask questions. If the new batch is not published yet or is already digested, report that and stop. Send notifications only when a new digest was written.
```

## Where to run it

- **Claude desktop app, scheduled tasks** (recommended): runs on your machine, so the working directory, config, ntfy files and digests are local and persistent. Create the task from the app, or ask Claude to create one with the scheduled-tasks tool using the prompt and cron expression above. The machine must be awake at the trigger times.
- **Plain cron or launchd** with `claude -p "<prompt>"` from the working directory, with the permission rules from the next section.
- **Cloud routines** (`/schedule`): these run in a remote checkout and do not see local files. Use them only if the config, digests and ntfy files live in a repository the routine can read and write.

## Permissions for unattended runs

An unattended run cannot answer permission prompts, so a step that needs one is skipped or fails. Run the skill once interactively and approve the recurring actions; or add allow rules to the project's `.claude/settings.local.json` for: Bash for `python3` with the plugin's scripts, `curl` to `https://ntfy.sh/...` and `osascript`; WebFetch for `arxiv.org`; the arXiv MCP server tools; Write under the digest directory; and the Artifact tool if you use the phone page. Keep each rule as narrow as you can.
