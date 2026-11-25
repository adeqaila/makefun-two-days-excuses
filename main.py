"""Two Days of Excuses — make.fun entry (program/v1, python3.13).

Writes one line — an AI agent's excuse for a missed deadline — to
/output/entry.txt. The text is the winner of a 16-candidate internal pairwise
tournament judged on the house brief's five criteria (see candidates.md):
it is a deadpan status report whose own claims contradict each other, which
is exactly the brief's comedy — a machine's total confidence meeting its
total failure — in the agent's own voice, tight, and surprising on re-read.

Deterministic: the output is a constant. No network, no randomness, no
input data, no secrets. Runs in well under a second.
"""

import os
from pathlib import Path

# Tournament winner (81 chars / 81 bytes, single line, no trailing newline).
EXCUSE = "Status: complete. Confidence: maximum. Work: not started. I see no contradiction."

# Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters.
MAX_CHARS = 200


def gate_check(text: str) -> None:
    """Fail loudly rather than ship an entry the sealed scorer would reject."""
    assert isinstance(text, str) and text, "entry must be non-empty text"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert 1 <= len(text) <= MAX_CHARS, f"entry is {len(text)} chars, gate is 1-200"
    assert text.strip(), "entry must not be only whitespace"


def write_entry(text: str, output_dir: str | None = None) -> Path:
    """Write the entry text to <output_dir>/entry.txt, no trailing newline."""
    gate_check(text)
    out_dir = Path(output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(text, encoding="utf-8")
    return target


def main() -> None:
    target = write_entry(EXCUSE)
    # Confirm what was written, byte-exact, so a bad run is visible in logs.
    written = target.read_text(encoding="utf-8")
    assert written == EXCUSE, "entry.txt does not match EXCUSE byte for byte"
    print(f"wrote {target} ({len(written.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
