"""Add original short, themed multiple-choice questions.

Each line in clue_style.txt is:
category|difficulty|question|correct|wrong|wrong|wrong
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANK = ROOT / "questions.json"
PACKS = sorted(ROOT.glob("clue_style_*.txt"))


def norm(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    seen = {norm(item["question"]) for item in bank}
    added = []
    skipped = 0
    lines = []
    for pack in PACKS:
        lines.extend(pack.read_text(encoding="utf-8").splitlines())
    for line_number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 7:
            raise SystemExit(f"Line {line_number} has {len(parts)} fields, expected 7")
        category, difficulty, question, correct, wrong_a, wrong_b, wrong_c = parts
        if difficulty not in {"easy", "medium", "hard"}:
            raise SystemExit(f"Line {line_number} has bad difficulty {difficulty}")
        choices = [correct, wrong_a, wrong_b, wrong_c]
        if len({choice.lower() for choice in choices}) != 4:
            raise SystemExit(f"Line {line_number} has repeated choices")
        if norm(question) in seen:
            skipped += 1
            continue
        seen.add(norm(question))
        added.append({
            "category": category,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct,
            "incorrect_answers": [wrong_a, wrong_b, wrong_c],
            "source": "original",
        })

    bank.extend(added)
    temporary = BANK.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(BANK)
    print(f"added {len(added)}")
    print(f"skipped repeats {skipped}")
    print(f"total {len(bank)}")


if __name__ == "__main__":
    main()
