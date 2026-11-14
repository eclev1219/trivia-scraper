"""Fill questions.json up to 20,000 after the first expansion pass.

Uses smaller Wikidata queries, then SciQ from the published parquet files.
"""

import os
import urllib.request

import pyarrow.parquet as pq

from expand_questions import (
    BIRTH_YEAR,
    BIRTH_YEAR_CAP,
    BLOCKED_QUESTION,
    DATABASE_FILE,
    RANDOM,
    TARGET,
    USER_AGENT,
    add_from_pool,
    add_record,
    by_links,
    clean_label,
    dedupe,
    load_questions,
    make_question,
    normalize,
    rows,
    save_questions,
    sciq_difficulty,
)

PARQUET_URLS = {
    "train": "https://huggingface.co/datasets/allenai/sciq/resolve/main/data/train-00000-of-00001.parquet",
    "validation": "https://huggingface.co/datasets/allenai/sciq/resolve/main/data/validation-00000-of-00001.parquet",
    "test": "https://huggingface.co/datasets/allenai/sciq/resolve/main/data/test-00000-of-00001.parquet",
}


def download(url, path):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response, open(path, "wb") as file:
        file.write(response.read())


def add_birth_years(questions, seen):
    occupations = (
        ("writers", "Q36180"),
        ("scientists", "Q901"),
        ("painters", "Q1028181"),
        ("composers", "Q36834"),
        ("monarchs", "Q116"),
        ("athletes", "Q2066131"),
    )
    found = []
    for name, occupation in occupations:
        if len(questions) >= TARGET:
            break
        print(f"Wikidata birth years: {name}...", flush=True)
        try:
            batch = rows(
                f"""
                SELECT ?itemLabel ?year ?links WHERE {{
                  ?item wdt:P106 wd:{occupation}; wdt:P569 ?birth; wikibase:sitelinks ?links.
                  FILTER(?links > 25)
                  BIND(YEAR(?birth) AS ?year)
                  FILTER(?year > 1600 && ?year < 1990)
                  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
                }}
                LIMIT 450
                """,
                ["itemLabel", "year", "links"],
            )
        except Exception as error:
            print(f"  skipped {name}: {error}", flush=True)
            continue
        print(f"  rows {len(batch)}", flush=True)
        found.extend(batch)

    people = {}
    for row in found:
        name = clean_label(row["itemLabel"])
        if name is None or not str(row["year"]).isdigit():
            continue
        year = int(row["year"])
        if not 1600 < year < 1990:
            continue
        key = normalize(name)
        if key not in people:
            people[key] = (name, year, int(float(row["links"])))
            continue
        previous = people[key]
        if previous is None or previous[1] != year:
            people[key] = None

    added = 0
    room = BIRTH_YEAR_CAP - sum(1 for item in questions if BIRTH_YEAR.search(item["question"]))
    for entry in people.values():
        if entry is None or len(questions) >= TARGET or added >= room:
            continue
        name, year, links = entry
        offsets = [-36, -21, -12, -7, 5, 9, 14, 23, 31]
        RANDOM.shuffle(offsets)
        incorrect = [str(year + offset) for offset in offsets if 1600 < year + offset < 1995][:3]
        if len(incorrect) != 3:
            continue
        record = make_question(
            "History",
            "easy" if links >= 80 else "medium" if links >= 40 else "hard",
            f"In which year was {name} born?",
            str(year),
            incorrect,
        )
        if add_record(questions, seen, record):
            added += 1
    print(f"  +{added} birth years (database now {len(questions)})", flush=True)


def add_sciq(questions, seen):
    added = 0
    for split, url in PARQUET_URLS.items():
        if len(questions) >= TARGET:
            break
        path = f"sciq-{split}.parquet"
        print(f"SciQ file: {split}...", flush=True)
        download(url, path)
        table = pq.read_table(path)
        for item in table.to_pylist():
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
        print(f"  SciQ added {added}; database {len(questions)}", flush=True)
    return added


def main():
    questions, seen = dedupe(load_questions())
    print(f"Starting from {len(questions)}", flush=True)
    before = len(questions)

    print("Wikidata: films...", flush=True)
    try:
        found = rows(
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q11424; wdt:P57 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 80)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 400
            """,
            ["itemLabel", "answerLabel", "links"],
        )
        pairs = [(row["itemLabel"], row["answerLabel"], int(float(row["links"]))) for row in found]
        added = add_from_pool(
            questions,
            seen,
            "Film & TV",
            pairs,
            lambda subject: f"Who directed the film {subject}?",
            by_links,
        )
        print(f"  +{added} (database now {len(questions)})", flush=True)
    except Exception as error:
        print(f"  skipped films: {error}", flush=True)

    print("Wikidata: continents...", flush=True)
    try:
        found = rows(
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q6256; wdt:P30 ?answer; wikibase:sitelinks ?links.
              FILTER NOT EXISTS { ?item wdt:P31 wd:Q3024240 }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            """,
            ["itemLabel", "answerLabel", "links"],
        )
        pairs = [(row["itemLabel"], row["answerLabel"], int(float(row["links"]))) for row in found]
        added = add_from_pool(
            questions,
            seen,
            "Geography",
            pairs,
            lambda subject: f"Which continent is {subject} on?",
            lambda links: "easy",
        )
        print(f"  +{added} (database now {len(questions)})", flush=True)
    except Exception as error:
        print(f"  skipped continents: {error}", flush=True)

    add_birth_years(questions, seen)
    save_questions(questions)
    add_sciq(questions, seen)
    save_questions(questions)
    print(f"Saved {len(questions)} unique questions (+{len(questions) - before}).", flush=True)


if __name__ == "__main__":
    main()
