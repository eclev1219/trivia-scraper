"""Grow questions.json to at least 20,000 unique multiple-choice questions.

New questions come from two places that allow reuse:
- Wikidata (CC0): public facts, with the question wording written here.
- SciQ (CC BY-NC 3.0): crowdsourced science questions from the Allen Institute for AI.

Questions already saved from Open Trivia DB and The Trivia API are kept.
Repeats are removed by comparing a normalized form of the question text.
"""

import json
import os
import random
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

DATABASE_FILE = "questions.json"
TARGET = 20000
BIRTH_YEAR_CAP = 900
BIRTH_YEAR = re.compile(r"(?:in which year was|what year was|when was).+ born", re.I)
USER_AGENT = "Trivianaut/1.0 (personal offline trivia; educational)"
RANDOM = random.Random(14)

LABEL_BAD = re.compile(r"[<>\[\]{}|\\@^*_=]|[\x00-\x1f]")


def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_label(value):
    if not value:
        return None
    value = " ".join(value.replace("\xa0", " ").split())
    if not 1 <= len(value) <= 72 or LABEL_BAD.search(value):
        return None
    if not any(char.isalpha() for char in value):
        return None
    if value.lower().startswith("category:"):
        return None
    if re.fullmatch(r"Q\d+", value):
        return None
    if re.search(r"https?://|wikidata\.org|well-known/genid", value, re.I):
        return None
    return value


def load_questions():
    with open(DATABASE_FILE, encoding="utf-8") as file:
        return json.load(file)


def save_questions(questions):
    temporary = DATABASE_FILE + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)
        file.write("\n")
    os.replace(temporary, DATABASE_FILE)


def dedupe(questions):
    kept = []
    seen = set()
    for item in questions:
        key = normalize(item["question"])
        if not key or key in seen:
            continue
        choices = [item["correct_answer"], *item["incorrect_answers"]]
        if len(item["incorrect_answers"]) != 3 or len({choice.strip().lower() for choice in choices}) != 4:
            continue
        seen.add(key)
        kept.append(item)
    return kept, seen


def sparql(query):
    request = urllib.request.Request(
        "https://query.wikidata.org/sparql",
        data=urllib.parse.urlencode({"query": query}).encode(),
        headers={
            "Accept": "application/sparql-results+json",
            "User-Agent": USER_AGENT,
        },
    )
    last_error = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            time.sleep(2 + attempt * 3)
    raise last_error


def rows(query, fields):
    data = sparql(query)
    found = []
    for binding in data["results"]["bindings"]:
        record = {}
        missing = False
        for field in fields:
            value = binding.get(field, {}).get("value", "")
            record[field] = value
            if not value:
                missing = True
        if not missing:
            found.append(record)
    return found


def make_question(category, difficulty, question, correct, incorrect):
    return {
        "category": category,
        "difficulty": difficulty,
        "question": question,
        "correct_answer": correct,
        "incorrect_answers": incorrect,
        "source": "Wikidata",
    }


def same_answer(left, right):
    return normalize(left) == normalize(right)


def answer_in_question(question, answer):
    return normalize(answer) in normalize(question)


def pick_distractors(answer, pool):
    choices = []
    seen = {normalize(answer)}
    order = list(pool)
    RANDOM.shuffle(order)
    for candidate in order:
        key = normalize(candidate)
        if not key or key in seen:
            continue
        seen.add(key)
        choices.append(candidate)
        if len(choices) == 3:
            return choices
    return None


def add_record(questions, seen, record):
    if len(questions) >= TARGET:
        return False
    key = normalize(record["question"])
    if not key or key in seen:
        return False
    if answer_in_question(record["question"], record["correct_answer"]):
        return False
    questions.append(record)
    seen.add(key)
    return True


def add_from_pool(questions, seen, category, pairs, question_for, difficulty_for):
    """pairs is a list of (subject, answer, links). Subjects with two answers are skipped."""
    grouped = {}
    for subject, answer, links in pairs:
        subject = clean_label(subject)
        answer = clean_label(answer)
        if subject is None or answer is None or same_answer(subject, answer):
            continue
        key = normalize(subject)
        bucket = grouped.get(key)
        if bucket is None:
            grouped[key] = {"subject": subject, "answers": [answer], "links": links}
            continue
        if not any(same_answer(answer, existing) for existing in bucket["answers"]):
            bucket["answers"].append(answer)
        bucket["links"] = max(bucket["links"], links)

    pool = [answer for bucket in grouped.values() if len(bucket["answers"]) == 1 for answer in bucket["answers"]]
    added = 0
    for bucket in grouped.values():
        if len(bucket["answers"]) != 1:
            continue
        subject = bucket["subject"]
        answer = bucket["answers"][0]
        question = question_for(subject)
        if answer_in_question(question, answer):
            continue
        incorrect = pick_distractors(answer, pool)
        if incorrect is None:
            continue
        record = make_question(
            category,
            difficulty_for(bucket["links"]),
            question,
            answer,
            incorrect,
        )
        if add_record(questions, seen, record):
            added += 1
    return added


def by_links(links):
    if links >= 80:
        return "easy"
    if links >= 25:
        return "medium"
    return "hard"


def collect_wikidata(questions, seen):
    jobs = [
        (
            "capitals",
            "Geography",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q6256; wdt:P36 ?answer; wikibase:sitelinks ?links.
              FILTER NOT EXISTS { ?item wdt:P31 wd:Q3024240 }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            """,
            lambda subject: f"What is the capital of {subject}?",
            lambda links: "easy" if links >= 40 else "medium",
        ),
        (
            "currencies",
            "Geography",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q6256; wdt:P38 ?answer; wikibase:sitelinks ?links.
              FILTER NOT EXISTS { ?item wdt:P31 wd:Q3024240 }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            """,
            lambda subject: f"What is the official currency of {subject}?",
            lambda links: "medium",
        ),
        (
            "languages",
            "Geography",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q6256; wdt:P37 ?answer; wikibase:sitelinks ?links.
              FILTER NOT EXISTS { ?item wdt:P31 wd:Q3024240 }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            """,
            lambda subject: f"What is the official language of {subject}?",
            lambda links: "medium",
        ),
        (
            "cities",
            "Geography",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q515; wdt:P17 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 40)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 1500
            """,
            lambda subject: f"In which country is {subject}?",
            by_links,
        ),
        (
            "mountains",
            "Geography",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q8502; wdt:P17 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 15)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 600
            """,
            lambda subject: f"In which country is {subject}?",
            by_links,
        ),
        (
            "lakes",
            "Geography",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q23397; wdt:P17 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 12)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 400
            """,
            lambda subject: f"In which country is {subject}?",
            by_links,
        ),
        (
            "elements",
            "Science & Nature",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q11344; wdt:P246 ?answer; wikibase:sitelinks ?links.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            """,
            lambda subject: f"What is the chemical symbol for {subject}?",
            lambda links: "easy" if links >= 70 else "medium",
        ),
        (
            "books",
            "Arts & Literature",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q7725634; wdt:P50 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 30)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 1200
            """,
            lambda subject: f"Who wrote {subject}?",
            by_links,
        ),
        (
            "films",
            "Film & TV",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q11424; wdt:P57 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 35)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 1200
            """,
            lambda subject: f"Who directed the film {subject}?",
            by_links,
        ),
        (
            "paintings",
            "Art",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q3305213; wdt:P170 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 20)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 800
            """,
            lambda subject: f"Who painted {subject}?",
            by_links,
        ),
        (
            "albums",
            "Music",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P31 wd:Q482994; wdt:P175 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 25)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 800
            """,
            lambda subject: f"Who recorded the album {subject}?",
            by_links,
        ),
        (
            "inventions",
            "History",
            """
            SELECT ?itemLabel ?answerLabel ?links WHERE {
              ?item wdt:P61 ?answer; wikibase:sitelinks ?links.
              FILTER(?links > 40)
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 500
            """,
            lambda subject: f"Who is credited with inventing {subject}?",
            by_links,
        ),
    ]

    for name, category, query, question_for, difficulty_for in jobs:
        if len(questions) >= TARGET:
            return
        print(f"Wikidata: {name}...", flush=True)
        try:
            found = rows(query, ["itemLabel", "answerLabel", "links"])
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"  skipped {name}: {error}", flush=True)
            continue
        pairs = []
        for row in found:
            try:
                links = int(float(row["links"]))
            except ValueError:
                links = 0
            pairs.append((row["itemLabel"], row["answerLabel"], links))
        added = add_from_pool(questions, seen, category, pairs, question_for, difficulty_for)
        print(f"  +{added} (database now {len(questions)})", flush=True)
        save_questions(questions)

    if len(questions) >= TARGET:
        return
    print("Wikidata: birth years...", flush=True)
    found = []
    for start, end, minimum_links in (
        (1500, 1700, 40),
        (1700, 1850, 40),
        (1850, 1920, 50),
        (1920, 1975, 60),
    ):
        try:
            found.extend(rows(
                f"""
                SELECT ?itemLabel ?year ?links WHERE {{
                  ?item wdt:P31 wd:Q5; wdt:P569 ?birth; wikibase:sitelinks ?links.
                  FILTER(?links > {minimum_links})
                  BIND(YEAR(?birth) AS ?year)
                  FILTER(?year >= {start} && ?year < {end})
                  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
                }}
                LIMIT 700
                """,
                ["itemLabel", "year", "links"],
            ))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"  skipped birth years {start}: {error}", flush=True)
    people = {}
    for row in found:
        name = clean_label(row["itemLabel"])
        if name is None or not re.fullmatch(r"\d{4}", row["year"]):
            continue
        year = int(row["year"])
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
        if entry is None or added >= room:
            continue
        name, year, links = entry
        offsets = [-42, -27, -16, -9, -5, 6, 11, 18, 29, 37]
        RANDOM.shuffle(offsets)
        incorrect = []
        for offset in offsets:
            candidate = year + offset
            if 1500 < candidate < 2000:
                incorrect.append(str(candidate))
            if len(incorrect) == 3:
                break
        if len(incorrect) != 3:
            continue
        record = make_question(
            "History",
            "easy" if links >= 120 else "medium" if links >= 80 else "hard",
            f"In which year was {name} born?",
            str(year),
            incorrect,
        )
        if add_record(questions, seen, record):
            added += 1
    print(f"  +{added} (database now {len(questions)})", flush=True)

    if len(questions) >= TARGET:
        return
    print("Wikidata: animal classes...", flush=True)
    class_query = """
    SELECT ?itemLabel ?classLabel ?links WHERE {
      VALUES ?class { wd:Q7377 wd:Q5113 wd:Q10811 wd:Q152 wd:Q10908 }
      ?item wdt:P31 wd:Q16521; wdt:P105 wd:Q7432; wdt:P171* ?class; wikibase:sitelinks ?links.
      FILTER(?links > 20)
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 1200
    """
    try:
        found = rows(class_query, ["itemLabel", "classLabel", "links"])
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"  skipped animals: {error}", flush=True)
        found = []
    class_names = {
        "mammal": "Mammals",
        "bird": "Birds",
        "reptile": "Reptiles",
        "fish": "Fish",
        "insect": "Insects",
    }
    animals = {}
    for row in found:
        name = clean_label(row["itemLabel"])
        group = class_names.get(row["classLabel"].lower())
        if name is None or group is None:
            continue
        key = normalize(name)
        if key not in animals:
            animals[key] = (name, group, int(float(row["links"])))
            continue
        previous = animals[key]
        if previous is None or previous[1] != group:
            animals[key] = None
    added = 0
    groups = list(class_names.values())
    for entry in animals.values():
        if entry is None:
            continue
        name, group, links = entry
        incorrect = [item for item in groups if item != group]
        record = make_question(
            "Animals",
            by_links(links),
            f"The {name.lower()} belongs to which animal group?",
            group,
            incorrect[:3],
        )
        if add_record(questions, seen, record):
            added += 1
    print(f"  +{added} (database now {len(questions)})", flush=True)


def sciq_rows(split):
    collected = []
    offset = 0
    while True:
        url = (
            "https://datasets-server.huggingface.co/rows"
            f"?dataset=allenai/sciq&config=default&split={split}&offset={offset}&length=100"
        )
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
        batch = payload.get("rows", [])
        if not batch:
            break
        collected.extend(row["row"] for row in batch)
        offset += len(batch)
        if offset >= payload.get("num_rows_total", offset):
            break
        time.sleep(0.15)
    return collected


BLOCKED_QUESTION = re.compile(
    r"\b(passage|paragraph|according to the (text|passage|article)|following sentence|graph above|table above)\b",
    re.I,
)


def sciq_difficulty(question):
    words = len(question.split())
    if words < 12:
        return "easy"
    if words < 22:
        return "medium"
    return "hard"


def collect_sciq(questions, seen):
    if len(questions) >= TARGET:
        return
    added = 0
    for split in ("train", "validation", "test"):
        print(f"SciQ: {split}...", flush=True)
        try:
            found = sciq_rows(split)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"  skipped {split}: {error}", flush=True)
            continue
        for item in found:
            if len(questions) >= TARGET:
                break
            question = " ".join(str(item.get("question", "")).split())
            correct = " ".join(str(item.get("correct_answer", "")).split())
            incorrect = [
                " ".join(str(item.get(f"distractor{number}", "")).split())
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
        print(f"  running total added from SciQ {added}; database {len(questions)}", flush=True)
        if len(questions) >= TARGET:
            break
    print(f"SciQ added {added}.", flush=True)


def main():
    questions, seen = dedupe(load_questions())
    print(f"After removing repeats: {len(questions)}", flush=True)
    before = len(questions)
    collect_wikidata(questions, seen)
    save_questions(questions)
    collect_sciq(questions, seen)
    save_questions(questions)
    print(f"Saved {len(questions)} unique questions (+{len(questions) - before}).", flush=True)


if __name__ == "__main__":
    main()
