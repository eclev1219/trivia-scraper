"""Drop later copies of the same fact, then top the bank back up to 20,000."""

import os
import re

import pyarrow.parquet as pq

from expand_questions import (
    BLOCKED_QUESTION,
    TARGET,
    USER_AGENT,
    add_record,
    dedupe,
    load_questions,
    normalize,
    save_questions,
    sciq_difficulty,
)
from top_up_questions import PARQUET_URLS, download

PATTERNS = (
    ("capital", re.compile(r"(?:what is the capital of|which of these is a capital of|capital city of|capital of) (.+)")),
    ("born", re.compile(r"(?:in which year was|what year was|when was) (.+) born")),
    ("wrote", re.compile(r"(?:who wrote|who is the author of|author of) (.+)")),
    ("country", re.compile(r"(?:in which country is|which country is) (.+?)(?: in)?$")),
    ("symbol", re.compile(r"(?:chemical symbol for|symbol for the element|symbol of) (.+)")),
    ("continent", re.compile(r"which continent is (.+) on")),
    ("currency", re.compile(r"(?:official currency of|currency of) (.+)")),
    ("language", re.compile(r"(?:official language of|language of) (.+)")),
    ("directed", re.compile(r"who directed the film (.+)")),
)


def fact_key(question):
    text = normalize(question)
    for kind, pattern in PATTERNS:
        match = pattern.search(text)
        if match:
            return (kind, match.group(1))
    return None


def drop_same_facts(questions):
    seen = {}
    kept = []
    removed = 0
    for item in questions:
        key = fact_key(item["question"])
        if key and key in seen:
            removed += 1
            continue
        if key:
            seen[key] = True
        kept.append(item)
    return kept, removed


def main():
    questions, _seen = dedupe(load_questions())
    questions, removed = drop_same_facts(questions)
    questions, seen = dedupe(questions)
    print(f"Removed {removed} repeated facts. Database is {len(questions)}.", flush=True)
    path = "sciq-train.parquet"
    download(PARQUET_URLS["train"], path)
    added = 0
    for item in pq.read_table(path).to_pylist():
        if len(questions) >= TARGET:
            break
        question = " ".join(str(item.get("question") or "").split())
        correct = " ".join(str(item.get("correct_answer") or "").split())
        incorrect = [
            " ".join(str(item.get(f"distractor{number}") or "").split())
            for number in (1, 2, 3)
        ]
        if len(question) < 20 or len(question) > 220 or BLOCKED_QUESTION.search(question):
            continue
        if not question.endswith("?"):
            question = question.rstrip(".") + "?"
        if not correct or any(not choice or len(choice) > 80 for choice in incorrect):
            continue
        if len({normalize(choice) for choice in [correct, *incorrect]}) != 4:
            continue
        record = {
            "category": "Science",
            "difficulty": sciq_difficulty(question),
            "question": question,
            "correct_answer": correct,
            "incorrect_answers": incorrect,
            "source": "SciQ",
        }
        if add_record(questions, seen, record):
            added += 1
    os.remove(path)
    save_questions(questions)
    print(f"Added {added} more science questions. Saved {len(questions)}.", flush=True)


if __name__ == "__main__":
    main()
