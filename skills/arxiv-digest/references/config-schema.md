# Config schema

Plain JSON. Search order, first match wins:

1. `.arxiv-digest/config.json` in the working directory
2. `~/.config/arxiv-digest/config.json`

Relative paths in the config resolve against the working directory. A complete example is in [../config.example.json](../config.example.json). The fetch script reads only `arxiv_subjects` and `arxiv_rss_base_url`; it ignores other fields.

## Focus profile

The profile is entirely the user's own words. Define it in either of two ways, or both:

- **One focus:** write `profile.tier_a` and `profile.tier_b`.
- **Several focus areas:** list them in `profile.focus_areas`, each with its own `tier_a` and `tier_b`. A paper earns the highest tier any area gives it, and the digest names the matching area on its entry.

When both are present, the global `tier_a` / `tier_b` act as a catch-all next to the areas. Everything not Tier A or B is Tier C.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `profile.role` | string | "researcher" | who the digest is for; sets the reading level |
| `profile.tier_a` | string | `""` | core: papers the user would drop everything to read |
| `profile.tier_b` | string | `""` | adjacent: worth a look |
| `profile.focus_areas` | `{name, tier_a, tier_b}[]` | `[]` | named focus areas, each triaged on its own descriptions; `tier_b` may be omitted |
| `profile.anchor_papers` | `{id, note}[]` | `[]` | papers central to the user's work; Tier A entries say how they relate to these |
| `profile.follow_authors` | string[] | `[]` | any paper by these authors is at least Tier B and is marked "followed author"; match on normalised family name plus initial, ignoring accents and TeX escapes |
| `profile.mute` | string[] | `[]` | kinds of paper that stay Tier C unless a `tier_a` description names them explicitly |
| `profile.examples` | `{id, tier, why}[]` | `[]` | past judgments by the user (`tier` is `A`, `B` or `C`); triage follows their pattern. Grows through the tuning flow in [setup.md](setup.md) |

Tier names are fixed (A, B, C) because the phone page finds sections by those headings. The words behind them are all yours.

## Everything else

| Field | Type | Default | Meaning |
|---|---|---|---|
| `arxiv_subjects` | string[] | required | arXiv feed codes, see [arxiv-categories.md](arxiv-categories.md) |
| `arxiv_rss_base_url` | string | `https://rss.arxiv.org/rss/` | feed base URL |
| `topics` | string[] | required | 2-5 short phrases summarising the focus; also lets tooling that expects this field reuse the file |
| `digest.dir` | string | `arxiv-digests` | where digests and `intermediate/` live |
| `digest.prefix` | string | first subject | digest file prefix: `<prefix>-YYYY-MM-DD.md` |
| `digest.language` | string | `English` | language of the digest text; section headings stay English because the page parses them |
| `digest.close_readings` | integer | `5` | maximum papers to read in depth; `0` disables close readings |
| `digest.include_cross_lists` | `none` \| `tier-a` \| `tier-a-and-b` \| `all` | `tier-a-and-b` | which cross-listed tiers appear in the digest |
| `digest.include_replacements` | same | `tier-a` | which replacement tiers appear |
| `site.enabled` | boolean | `false` | build and publish the phone page |
| `site.title` | string | `<prefix> digest` | page title |
| `site.kicker` | string | `arXiv <prefix> · announcement` | small line above the date on the page |
| `site.artifact_url` | string | `""` | claude.ai Artifact to republish; empty means build the file only |
| `notify.ntfy_topic_file` | string | unset | file holding the private ntfy topic name (one line); unset disables ntfy |
| `notify.ntfy_click_file` | string | unset | file holding the URL a tap on the notification opens (one line) |
| `notify.mac_banner` | boolean | `false` | macOS notification banner (macOS only) |

Keep secrets out of this file: the ntfy topic lives in its own file (it works like a password on the public ntfy.sh server), so the config can be shared with a colleague. Drop the `site` block first, since `site.artifact_url` points at your own page.
