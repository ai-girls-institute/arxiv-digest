# Digest file format

The digest is read on a small phone screen and rendered by `assets/site-template.html`. The page finds sections by their level-2 heading text, so keep **exactly** this structure, with these headings, in this order:

```
# <prefix> digest, announced YYYY-MM-DD
## At a glance
## Statistics
## Tier A
## Tier B
## Close readings
## Everything else (Tier C, new submissions)
```

The page matches headings by prefix (`Tier A`, `Tier B`, `At a glance`, `Statistics`, `Close readings`, `Everything else`); the level-1 title line is ignored by the page. Write "None today." under an empty tier.

## Language

Write the digest text in `digest.language` (default English), including the bold labels. Only the six section headings above stay in English, because the page finds sections by them.

## Formatting rules

- **Math.** Write every formula, symbol or expression with sub- or superscripts as LaTeX between single dollar signs: `$A_n(z)$`, `$\mathrm{Tr}\,\phi^3$`, `$SU(2)/U(1)$`. A display equation is `$$...$$` on one source line with a blank line before and after, only when short and essential. Never write underscores or carets outside dollar signs. Use a dollar sign for nothing but math (write USD or "dollars" otherwise).
- **Paragraphs** are at most 3 sentences.
- **arXiv IDs** are written plain (2610.08566) so they become tappable.

## Section content

**At a glance** (at most 8 bullet lines): the number of Tier A/B papers including cross-lists; then the 3-5 most relevant items for the user, one sentence each, leading with the arXiv ID; then one line on any notable trend or big result elsewhere that day.

**Statistics**: one markdown table with columns `Group | Announced | Reviewed | Shown | Tier A | Tier B | Tier C` and rows `New submissions`, `Cross-lists`, `Replacements`, `Total`. Tier C counts for cross-lists and replacements are papers judged Tier C but not shown. Below the table, one short paragraph of source and coverage notes: data source and date check, failed feeds, abstract-only entries, reading depth.

**Tier A**, then **Tier B**: a bullet list, one bullet per paper. Each bullet is made of separate paragraphs (blank line between them, each indented under the bullet) in this order:

1. the title as a markdown link to `https://arxiv.org/abs/<id>`;
2. one metadata line: authors, arXiv ID, label (`new`, `cross-list (<primary archive>)`, or `replacement`), then, where they apply, the matching focus area (when the profile has several) and "followed author";
3. two concrete sentences on the question and the main result, ending with "(abstract-based)" unless a close reading exists;
4. Tier A only: a paragraph starting with the bold word **Relation** and one line on how the paper relates to the profile's anchor papers and focus (extends, competes with, applies, or merely adjacent). If the profile has no anchor papers, relate it to the focus alone.

**Close readings**: for each close-read paper, a level-3 heading `### <arXiv ID> · <short title>`, then short paragraphs that each start with a bold label: **Question.** (1-2 sentences), **Result.** (the main claim, with equation or section references such as Eq. 3.5, Sec. 4), **Scope and limits.** (proved versus conjectured or numerical, assumptions, what the paper does not cover), **Relation to your focus.** (1-2 sentences), **Read.** (sections actually read, sections not read). 100-150 words per paper in total.

**Everything else (Tier C, new submissions)**: every remaining NEW paper as one bullet: the title as a markdown link to `https://arxiv.org/abs/<id>`, then authors, arXiv ID and one sentence, grouped under short level-3 topic headings (for example holography, strings, cosmology, QFT, math-phys, or whatever fits the subject).

## Completeness

Every NEW paper appears exactly once. Cross-lists and replacements appear only if the config allows their tier. The Statistics table and the listing-page counts must agree.
