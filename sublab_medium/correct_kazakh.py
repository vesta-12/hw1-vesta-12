"""Sublab Medium - one Kazakh-correction task, six models.

Six models, one prompt, eight sentences. What you are producing is evidence:
a table that says which models repaired which kind of damage, and what each one
charged you for the attempt.

Fill in every `TODO`. Keep the function signatures.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sublab_easy.registration_bot import (RATES_PER_MTOK,  # noqa: E402
                                          ask_once, estimate_cost)

DATA = Path(__file__).resolve().parent.parent / "data" / "kazakh_errors.json"

# Every model you must run. Keep the order - it is the order of your table.
MODELS = [
    ("openrouter", "poolside/laguna-s-2.1:free"),
    ("openrouter", "inclusionai/ling-3.0-flash-vl:free"),
    ("openrouter", "dots-studio/dots-3-note-preview:free"),
    ("openai", "gpt-5.6-luna"),
    ("openai", "gpt-5.6-terra"),
    ("openai", "gpt-5.6-sol"),
]


def load_sentences() -> list[dict]:
    """The eight corrupted sentences and their published originals."""
    return json.loads(DATA.read_text(encoding="utf-8"))["sentences"]


def build_prompt(corrupted: str) -> str:
    """Ask for a corrected sentence AND a list of the changes made.

    Requirements:
      - state that the text is Kazakh and may contain wrong letters, joined
        words, or letters from the wrong alphabet;
      - demand exactly this JSON and nothing else:
            {"corrected": "...", "changes": ["...", "..."]}
      - do not include the correct answer in the prompt. You are testing the
        model, not your own typing.

    Asking for a fixed shape instead of prose is how you make six models
    comparable. Week 3 turns this into a topic.
    """
    return f"""Correct the following Kazakh sentence.

    The text may contain incorrect letters, joined words, missing hyphens,
    doubled letters, or visually similar letters from the wrong alphabet.

    Return exactly one JSON object and nothing else in this format:
    {{"corrected": "...", "changes": ["...", "..."]}}

    In "corrected", write the fully corrected Kazakh sentence.
    In "changes", briefly list what you changed.

    Sentence:
    {corrupted}"""


def parse_response(text: str) -> dict:
    """Pull {"corrected": str, "changes": list} out of the model's reply."""

    decoder = json.JSONDecoder()

    for i, char in enumerate(text):
        if char != "{":
            continue

        try:
            obj, _ = decoder.raw_decode(text[i:])
        except json.JSONDecodeError:
            continue

        if (
            isinstance(obj, dict)
            and isinstance(obj.get("corrected"), str)
            and isinstance(obj.get("changes"), list)
        ):
            return {
                "corrected": obj["corrected"],
                "changes": obj["changes"],
            }

    raise ValueError(f"No valid correction JSON found in response: {text!r}")


def correct_with(model: str, corrupted: str, via: str) -> dict:
    """Send one sentence to one model."""

    prompt = build_prompt(corrupted)

    response = ask_once(
        prompt,
        model=model,
        via=via
    )

    parsed = parse_response(response["text"])

    return {
        "corrected": parsed["corrected"],
        "changes": parsed["changes"],
        "input_tokens": response["input_tokens"],
        "output_tokens": response["output_tokens"],
        "model": response["model"],
    }


def score_correction(returned: str, expected: str) -> dict:
    """Compare a model's output against the published original."""

    positional_diff = sum(
        returned_char != expected_char
        for returned_char, expected_char in zip(returned, expected)
    )

    length_diff = abs(len(returned) - len(expected))

    return {
        "exact": returned == expected,
        "char_diff": positional_diff + length_diff,
    }


def run_all() -> list[dict]:
    """Every model against every sentence. One row per (model, sentence)."""
    rows = []
    for via, model in MODELS:
        for s in load_sentences():
            try:
                r = correct_with(model, s["corrupted"], via)
            except Exception as exc:            # a model failing IS a result
                rows.append({"model": model, "id": s["id"],
                             "errors": s["errors"], "failed": repr(exc)})
                continue
            rate_in, rate_out = RATES_PER_MTOK[model]
            rows.append({
                "model": model,
                "id": s["id"],
                "errors": s["errors"],
                "corrected": r["corrected"],
                "changes": r["changes"],
                **score_correction(r["corrected"], s["correct"]),
                "cost": estimate_cost(r["input_tokens"], r["output_tokens"],
                                      rate_in, rate_out),
                "input_tokens": r["input_tokens"],
                "output_tokens": r["output_tokens"],
            })
    return rows


def summarise(rows: list[dict]) -> None:
    """Per-model totals, to paste into SUBMISSION.md."""
    print(f"{'model':38}{'exact':>7}{'failed':>8}{'tokens':>9}{'cost $':>10}")
    print("-" * 72)
    for _, model in MODELS:
        mine = [r for r in rows if r["model"] == model]
        exact = sum(1 for r in mine if r.get("exact"))
        failed = sum(1 for r in mine if r.get("failed"))
        toks = sum(r.get("input_tokens", 0) + r.get("output_tokens", 0) for r in mine)
        cost = sum(r.get("cost", 0.0) for r in mine)
        print(f"{model:38}{exact:>7}{failed:>8}{toks:>9}{cost:>10.5f}")


if __name__ == "__main__":
    out = run_all()
    summarise(out)
    dest = Path(__file__).resolve().parent.parent / "outputs"
    dest.mkdir(exist_ok=True)
    (dest / "corrections.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote outputs/corrections.json ({len(out)} rows)")
