# Setup and tuning

Run the setup when no config exists and the session is interactive. Ask with AskUserQuestion where it fits; plain-text questions otherwise. Never skip a step silently. The focus profile is the user's own: draft it from what they tell you, show it, and let them edit it until it reads right.

## 1. Subjects

Ask which arXiv feeds to follow. Offer a few common groups (for example `cs.CL + cs.LG`, `hep-th`, `math-ph + hep-th`) and accept free text. Map answers to feed codes with [arxiv-categories.md](arxiv-categories.md) and confirm the codes you picked. Each feed is one request and every paper is triaged, so prefer a few focused feeds over a whole archive on a busy day.

## 2. Focus

Offer three ways to describe it, whichever is easiest for the user:

- **In words:** "Describe what you work on and what you would drop everything to read."
- **From papers:** the arXiv IDs of 3-5 of the user's own papers, or papers they wish they had written. Read their abstracts (MCP `get_abstract`, or `https://arxiv.org/abs/<id>`) and infer the focus, then say what you inferred.
- **From a colleague:** a `config.json` someone shared. Keep its `profile`, `topics` and `arxiv_subjects`, and ask what the user wants to change.

Then draft:

- `topics`: 2-5 short phrases;
- `profile.role`: one phrase, which sets the reading level of the digest;
- either one `tier_a` / `tier_b` pair, or several `profile.focus_areas` when the user works on distinct strands. Suggest focus areas when the description clearly has more than one thread; each gets a short name and its own tier text;
- Tier text works best when specific ("graph neural network expressivity, oversmoothing, and their spectral analysis") rather than broad ("machine learning"). Tier A is "drop everything", Tier B is "worth a look".

Then ask, each optional:

- **Anchor papers:** 0-3 arXiv IDs central to the work. Look up each title and store `{id, note}`.
- **Followed authors:** people whose every paper the user wants to see; stored in `follow_authors`.
- **Muted kinds:** what the user never wants in Tier A or B, for example "papers that only apply a known method to a new dataset"; stored in `mute`.
- **Language:** if not English, set `digest.language`.

## 3. Output

Choose the digest folder (default `arxiv-digests`) and file prefix (default: the first subject). Digests are plain Markdown, one file per announcement day.

## 4. Extras (each optional, default off)

- Phone page: sets `site.enabled`. Build it once with the command in [notifications.md](notifications.md), then publish it as a **private** Artifact (the first publish is the only step that creates one) and store the returned URL in `site.artifact_url`.
- Notifications: see [notifications.md](notifications.md). Never print the ntfy topic back into chat.
- Schedule: see [scheduling.md](scheduling.md).

## 5. Write and confirm

Create `.arxiv-digest/config.json` (shape: [../config.example.json](../config.example.json), fields: [config-schema.md](config-schema.md)) in the working directory, or `~/.config/arxiv-digest/config.json` if the user wants one profile everywhere. Omit fields the user left empty. If the project is a git repository, suggest adding `.arxiv-digest/ntfy-*` to `.gitignore`. Then run the first digest and invite feedback on the tiers (below).

## Changing the profile later

Edit the config in place, show a short before/after of what changed, and save only after the user agrees. Never touch `notify` or `site` unless asked.

- **Add, rename or remove a focus area, anchor, followed author or muted kind:** change the matching field.
- **"That paper is in the wrong tier"** (the usual way a profile improves): ask in one line why, then do the smallest fix that explains it:
  - the reason is about a kind of paper: rewrite the relevant `tier_a` / `tier_b` text, or add a `mute` entry;
  - the reason is a judgement call that words do not capture well: add `{id, tier, why}` to `profile.examples`;
  - the paper is from a person the user wants more of: add to `follow_authors`.
  Keep `examples` to the 10-15 most telling cases; when adding past that, drop the least informative.
- **Triage feels too wide or too narrow:** tighten or loosen the tier text rather than adding a threshold; if Tier A is overcrowded, make `tier_a` stricter and move the loose part to `tier_b`.
- **Share a profile:** send a colleague `.arxiv-digest/config.json` with the `site` block removed (`site.artifact_url` points at the user's own page). It holds no secrets, because the ntfy topic is in its own file; they drop it into their own project and adjust it.

One-off requests ("just check cs.CY today", "this week only look for X") are overrides for that run and are not saved unless the user asks.
