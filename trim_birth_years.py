"""Keep 900 birth-year questions and refill the bank to 20,000 with SciQ."""

import os
import random
import tempfile

import pyarrow.parquet as pq

from expand_questions import (
    BIRTH_YEAR,
    BLOCKED_QUESTION,
    TARGET,
    add_record,
    dedupe,
    load_questions,
    normalize,
    save_questions,
    sciq_difficulty,
)
from top_up_questions import PARQUET_URLS, download

KEEP_BIRTH_YEARS = 900


def add_sciq_until_full(questions, seen):
    added = 0
    for split, url in PARQUET_URLS.items():
        if len(questions) >= TARGET:
            break
        handle, path = tempfile.mkstemp(suffix=".parquet")
        os.close(handle)
        print(f"SciQ file: {split}...", flush=True)
        try:
            download(url, path)
            rows = pq.read_table(path).to_pylist()
        except Exception as error:
            print(f"  skipped {split}: {error}", flush=True)
            rows = []
        finally:
            if os.path.exists(path):
                os.remove(path)
        for item in rows:
            if len(questions) >= TARGET:
                break
            question = " ".join(str(item.get("question") or "").split())
            correct = " ".join(str(item.get("correct_answer") or "").split())
            incorrect = [
                " ".join(str(item.get(f"distractor{number}") or "").split())
                for number in (1, 2, 3)
            ]
            if BIRTH_YEAR.search(question):
                continue
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
        print(f"  bank is {len(questions)}", flush=True)
    return added


def main():
    questions, _seen = dedupe(load_questions())
    births = [item for item in questions if BIRTH_YEAR.search(item["question"])]
    rest = [item for item in questions if not BIRTH_YEAR.search(item["question"])]
    random.Random(14).shuffle(births)
    kept = births[:KEEP_BIRTH_YEARS]
    questions = rest + kept
    questions, seen = dedupe(questions)
    print(f"Birth years {len(births)} -> {len(kept)}. Bank {len(questions)}.", flush=True)
    added = add_sciq_until_full(questions, seen)
    save_questions(questions)
    remaining = sum(1 for item in questions if BIRTH_YEAR.search(item["question"]))
    print(f"Saved {len(questions)}. SciQ added {added}. Birth years now {remaining}.", flush=True)


if __name__ == "__main__":
    main()
