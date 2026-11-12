"""Compare a back-translation with its fixed reference using only the standard library."""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


TOKEN = re.compile(r"\w+(?:['’‘-]\w+)*|[^\w\s]")
APOSTROPHES = str.maketrans({"’": "'", "‘": "'"})
KINDS = {"insert": "missing", "delete": "extra", "replace": "different"}


def span(text, tokens, left, right):
    """Use zero-based, end-exclusive character positions in the original text."""
    start = tokens[left].start() if left < len(tokens) else len(text.rstrip())
    end = tokens[right - 1].end() if right > left else start
    return {
        "start": start,
        "end": end,
        "line": text.count("\n", 0, start) + 1,
        "text": text[start:end],
    }


def compare(reference, draft, threshold=90):
    if not isinstance(reference, str) or not isinstance(draft, str):
        raise ValueError("reference and draft must be strings")
    if not 0 <= threshold <= 100:
        raise ValueError("threshold must be between 0 and 100")
    expected = list(TOKEN.finditer(reference))
    actual = list(TOKEN.finditer(draft))
    if not expected:
        raise ValueError("reference must contain text")
    matcher = SequenceMatcher(
        None,
        [token.group().translate(APOSTROPHES) for token in actual],
        [token.group().translate(APOSTROPHES) for token in expected],
        autojunk=False,
    )
    differences = []
    for kind, left, right, ref_left, ref_right in matcher.get_opcodes():
        if kind == "equal":
            continue
        differences.append({
            "type": KINDS[kind],
            "draft": span(draft, actual, left, right),
            "reference": span(reference, expected, ref_left, ref_right),
        })
    score = matcher.ratio() * 100
    status = "needs_revision"
    if not actual:
        status = "empty"
    elif not differences:
        status = "exact"
    elif score >= threshold:
        status = "close"
    return {
        "similarity_percent": round(score, 2),
        "text_status": status,
        "threshold": threshold,
        "reference_tokens": len(expected),
        "draft_tokens": len(actual),
        "matched_tokens": sum(block.size for block in matcher.get_matching_blocks()),
        "normalization": "Ignore whitespace and straight/curly apostrophe differences; retain case and punctuation.",
        "differences": differences,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="UTF-8 JSON with reference and draft; default stdin")
    parser.add_argument("--threshold", type=float, default=90)
    args = parser.parse_args()
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        text = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
        data = json.loads(text)
        if not isinstance(data, dict) or "reference" not in data or "draft" not in data:
            raise ValueError("input must be an object containing reference and draft")
        result = compare(data["reference"], data["draft"], args.threshold)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot compare input: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
