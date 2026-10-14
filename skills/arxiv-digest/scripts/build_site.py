#!/usr/bin/env python3
"""Build a single self-contained phone-friendly HTML page from the saved digests.

Usage:
    python3 build_site.py --digests-dir DIR --prefix hep-th \
        [--title "hep-th Digest"] [--kicker "arXiv hep-th · announcement"] [--output FILE]

Reads every DIR/<prefix>-YYYY-MM-DD.md (newest first), embeds them in
../assets/site-template.html and writes DIR/site/index.html (or --output).
Standard library only.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "site-template.html"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--digests-dir", required=True, help="folder holding <prefix>-YYYY-MM-DD.md files")
    ap.add_argument("--prefix", required=True, help="digest file prefix, e.g. hep-th")
    ap.add_argument("--title", help="page <title> (default: '<prefix> digest')")
    ap.add_argument("--kicker", help="small line above the date (default: 'arXiv <prefix> · announcement')")
    ap.add_argument("--output", help="output file (default: <digests-dir>/site/index.html)")
    args = ap.parse_args()

    root = Path(args.digests_dir).expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"error: digests dir not found: {root}")
    pattern = re.compile(rf"{re.escape(args.prefix)}-(\d{{4}}-\d{{2}}-\d{{2}})\.md")

    digests = []
    for p in sorted(root.glob(f"{args.prefix}-*.md"), reverse=True):
        m = pattern.fullmatch(p.name)
        if m:
            digests.append({"date": m.group(1), "md": p.read_text(encoding="utf-8")})
    if not digests:
        sys.exit(f"error: no {args.prefix}-YYYY-MM-DD.md files in {root}")

    title = args.title or f"{args.prefix} digest"
    kicker = args.kicker or f"arXiv {args.prefix} · announcement"
    out = Path(args.output).expanduser() if args.output else root / "site" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    def js_single_quoted(s):  # the template puts the kicker inside '...' in a script
        return json.dumps(s, ensure_ascii=False)[1:-1].replace("'", "\\'").replace("</", "<\\/")

    html = TEMPLATE.read_text(encoding="utf-8")
    blob = json.dumps(digests, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*DIGESTS_JSON*/[]", blob)
    html = html.replace("/*BUILT_AT*/", datetime.now().strftime("%Y-%m-%d %H:%M"))
    html = html.replace("/*SITE_TITLE*/", escape(title))
    html = html.replace("/*SITE_KICKER*/", js_single_quoted(kicker))
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} with {len(digests)} digest(s), {len(html)} bytes")


if __name__ == "__main__":
    main()
