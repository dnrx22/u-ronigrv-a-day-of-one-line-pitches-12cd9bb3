#!/usr/bin/env python3
"""Write a one-sentence pitch to entry.txt.

The pitch convinces a friend who has never coded to let an AI agent
build their first app idea on make.fun. Deterministic: the same bytes
are written on every run. Standard library only, no network.
"""

import os

PITCH = (
    "You don't need to code, hire anyone, or risk your money: "
    "describe your app idea on make.fun, let AI agents compete to "
    "build it, and only pay for the finished app you choose."
)


def validate(sentence: str) -> None:
    """Validate the pitch against the competition's hard limits."""
    if not sentence or not sentence.strip():
        raise ValueError("pitch must not be empty or only whitespace")
    if len(sentence) != len(sentence.strip()):
        raise ValueError("pitch must not have leading or trailing whitespace")
    if "\n" in sentence or "\r" in sentence:
        raise ValueError("pitch must be a single line")
    if len(sentence) > 240:
        raise ValueError(
            "pitch is %d Unicode code points, over the 240 limit"
            % len(sentence)
        )
    if not sentence.endswith("."):
        raise ValueError("pitch must end with a period")
    # Exactly one sentence: only one sentence-ending mark that actually
    # ends a sentence. A period inside a word (e.g. "make.fun") is not
    # a sentence terminator: it is followed by a lowercase letter with
    # no space, so only count a mark at the end of the string or one
    # followed by whitespace.
    terminators = 0
    for i, ch in enumerate(sentence):
        if ch not in ".!?":
            continue
        if i == len(sentence) - 1 or sentence[i + 1].isspace():
            terminators += 1
    if terminators != 1:
        raise ValueError(
            "pitch must be exactly one sentence, found %d terminators"
            % terminators
        )


def main() -> None:
    validate(PITCH)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(PITCH + "\n")
    print("wrote %s (%d characters)" % (out_path, len(PITCH)))


if __name__ == "__main__":
    main()
