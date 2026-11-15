"""Rebalance questions.json to about 28,000 questions.

Crowded categories are trimmed. Short categories are filled with new
multiple-choice questions written here from public Wikidata facts (CC0).
General Knowledge is kept larger than the other categories. Birth-year
questions are not added.
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
USER_AGENT = "Trivianaut/1.0 (personal offline trivia; educational)"
RANDOM = random.Random(28)
GK_CAP = 3400
OTHER_CAP = 1900
DIFFICULTIES = ("easy", "medium", "hard")
BIRTH_YEAR = re.compile(r"(?:in which year was|what year was|when was).+ born", re.I)
LABEL_BAD = re.compile(r"[<>\[\]{}|\\@^*_=]|[\x00-\x1f]")
SOURCE_RANK = {
    "original": 0,
    "Open Trivia DB": 1,
    "The Trivia API": 2,
    "Wikidata": 4,
    "SciQ": 5,
}


def bucket_of(name):
    if not name:
        return "General Knowledge"
    if name in ("Film & TV", "Music", "Celebrities") or name.startswith("Entertainment:"):
        return "Entertainment"
    if name in ("Science", "Science & Nature") or name.startswith("Science:"):
        return "Science"
    if name in ("Sports", "Sport & Leisure"):
        return "Sports"
    return name


def cap_for(bucket):
    return GK_CAP if bucket == "General Knowledge" else OTHER_CAP


def quotas():
    limits = {}
    for bucket in (
        "General Knowledge",
        "Animals",
        "Art",
        "Arts & Literature",
        "Entertainment",
        "Food & Drink",
        "Geography",
        "History",
        "Mythology",
        "Politics",
        "Science",
        "Society & Culture",
        "Sports",
        "Vehicles",
    ):
        cap = cap_for(bucket)
        base, extra = divmod(cap, 3)
        limits[bucket] = {difficulty: base + (1 if index < extra else 0) for index, difficulty in enumerate(DIFFICULTIES)}
    return limits


def normalize(text):
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().replace("\u2019", "'").replace("`", "'")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_label(value):
    if not value:
        return None
    value = " ".join(str(value).replace("\xa0", " ").split())
    if not 1 <= len(value) <= 80 or LABEL_BAD.search(value):
        return None
    if not any(char.isalpha() for char in value):
        return None
    lowered = value.lower()
    if lowered.startswith("category:") or lowered in {"unknown", "none", "n/a", "human", "taxon"}:
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
        key = normalize(item.get("question", ""))
        choices = [item.get("correct_answer", ""), *item.get("incorrect_answers", [])]
        if not key or key in seen:
            continue
        if len(item.get("incorrect_answers", [])) != 3:
            continue
        if len({normalize(choice) for choice in choices if str(choice).strip()}) != 4:
            continue
        if item.get("difficulty") not in DIFFICULTIES:
            item["difficulty"] = "medium"
        seen.add(key)
        kept.append(item)
    return kept, seen


def priority(item):
    rank = SOURCE_RANK.get(item.get("source"), 3)
    if BIRTH_YEAR.search(item.get("question", "")):
        rank += 3
    return rank


def trim(questions):
    limits = quotas()
    grouped = {}
    for item in questions:
        grouped.setdefault(bucket_of(item.get("category")), {}).setdefault(item["difficulty"], []).append(item)
    kept = []
    for bucket, by_diff in grouped.items():
        limit = limits.get(bucket)
        if limit is None:
            for items in by_diff.values():
                kept.extend(items)
            continue
        for difficulty, items in by_diff.items():
            RANDOM.shuffle(items)
            items.sort(key=priority)
            kept.extend(items[: limit.get(difficulty, 0)])
    return kept


def room_left(counts):
    limits = quotas()
    remaining = {}
    for bucket, limit in limits.items():
        remaining[bucket] = {}
        have = counts.get(bucket, {})
        for difficulty, cap in limit.items():
            remaining[bucket][difficulty] = max(0, cap - have.get(difficulty, 0))
    return remaining


def count_cells(questions):
    counts = {}
    for item in questions:
        bucket = bucket_of(item.get("category"))
        cell = counts.setdefault(bucket, {})
        cell[item["difficulty"]] = cell.get(item["difficulty"], 0) + 1
    return counts


def sparql(query):
    request = urllib.request.Request(
        "https://query.wikidata.org/sparql",
        data=urllib.parse.urlencode({"query": query}).encode(),
        headers={"Accept": "application/sparql-results+json", "User-Agent": USER_AGENT},
    )
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=70) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            time.sleep(3 + attempt * 4)
    raise last_error


def rows(query):
    data = sparql(query)
    found = []
    for binding in data["results"]["bindings"]:
        record = {field: value.get("value", "") for field, value in binding.items()}
        if record.get("itemLabel") and record.get("answerLabel"):
            found.append(record)
    return found


def choose_difficulty(remaining, bucket, preferred):
    cell = remaining.get(bucket)
    if not cell:
        return None
    if cell.get(preferred, 0) > 0:
        return preferred
    for difficulty in ("medium", "easy", "hard"):
        if cell.get(difficulty, 0) > 0:
            return difficulty
    return None


def pick_distractors(answer, pool):
    chosen = []
    seen = {normalize(answer)}
    order = list(pool)
    RANDOM.shuffle(order)
    for candidate in order:
        key = normalize(candidate)
        if not key or key in seen:
            continue
        seen.add(key)
        chosen.append(candidate)
        if len(chosen) == 3:
            return chosen
    return None


def add_from_rows(questions, seen, remaining, bucket, found, question_for, preferred_for):
    grouped = {}
    for row in found:
        subject = clean_label(row.get("itemLabel"))
        answer = clean_label(row.get("answerLabel"))
        if subject is None or answer is None or normalize(subject) == normalize(answer):
            continue
        try:
            links = int(float(row.get("links") or 0))
        except ValueError:
            links = 0
        key = normalize(subject)
        current = grouped.get(key)
        if current is None:
            grouped[key] = {"subject": subject, "answers": [answer], "links": links}
            continue
        if not any(normalize(answer) == normalize(existing) for existing in current["answers"]):
            current["answers"].append(answer)
        current["links"] = max(current["links"], links)

    singles = [item for item in grouped.values() if len(item["answers"]) == 1]
    pool = [item["answers"][0] for item in singles]
    added = 0
    RANDOM.shuffle(singles)
    for item in singles:
        if sum(remaining.get(bucket, {}).values()) <= 0:
            break
        subject = item["subject"]
        answer = item["answers"][0]
        question = question_for(subject)
        if normalize(answer) in normalize(question):
            continue
        preferred = preferred_for(item["links"])
        difficulty = choose_difficulty(remaining, bucket, preferred)
        if difficulty is None:
            break
        incorrect = pick_distractors(answer, pool)
        if incorrect is None:
            continue
        key = normalize(question)
        if not key or key in seen:
            continue
        questions.append({
            "category": bucket,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": answer,
            "incorrect_answers": incorrect,
            "source": "Wikidata",
        })
        seen.add(key)
        remaining[bucket][difficulty] -= 1
        added += 1
    return added


def by_links(links):
    if links >= 80:
        return "easy"
    if links >= 25:
        return "medium"
    return "hard"


JOBS = [
    (
        "dishes",
        "Food & Drink",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q746549; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 2)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1500
        """,
        lambda subject: f"Which country is {subject} most associated with?",
        lambda links: "easy" if links >= 20 else "medium",
    ),
    (
        "ingredients",
        "Food & Drink",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q746549; wdt:P186 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 2)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1200
        """,
        lambda subject: f"Which ingredient is used to make {subject}?",
        lambda links: "medium" if links >= 15 else "hard",
    ),
    (
        "scientific names",
        "Animals",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q16521; wdt:P225 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 8)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 2200
        """,
        lambda subject: f"What is the scientific name of the {subject}?",
        lambda links: "medium" if links >= 40 else "hard",
    ),
    (
        "dog breeds",
        "Animals",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q39367; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 3)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 800
        """,
        lambda subject: f"Which country is the {subject} dog breed associated with?",
        lambda links: "easy" if links >= 25 else "medium",
    ),
    (
        "conservation",
        "Animals",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q16521; wdt:P141 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 12)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1500
        """,
        lambda subject: f"What is the conservation status of the {subject}?",
        by_links,
    ),
    (
        "paintings",
        "Art",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q3305213; wdt:P170 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 6)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 2000
        """,
        lambda subject: f"Who painted {subject}?",
        by_links,
    ),
    (
        "museums",
        "Art",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q3305213; wdt:P195 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 6)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1500
        """,
        lambda subject: f"Which museum holds the painting {subject}?",
        lambda links: "medium" if links >= 30 else "hard",
    ),
    (
        "books",
        "Arts & Literature",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q7725634; wdt:P50 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 12)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1800
        """,
        lambda subject: f"Who wrote {subject}?",
        by_links,
    ),
    (
        "cars",
        "Vehicles",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q3231690; wdt:P176 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 4)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 2000
        """,
        lambda subject: f"Which company makes the {subject}?",
        lambda links: "easy" if links >= 30 else "medium",
    ),
    (
        "aircraft",
        "Vehicles",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q15056993; wdt:P176 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 4)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1200
        """,
        lambda subject: f"Which company built the {subject}?",
        lambda links: "medium" if links >= 20 else "hard",
    ),
    (
        "stadiums",
        "Sports",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q483110; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 8)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1200
        """,
        lambda subject: f"In which country is {subject}?",
        lambda links: "easy" if links >= 25 else "medium",
    ),
    (
        "deities",
        "Mythology",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q178885; wdt:P361 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 4)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1500
        """,
        lambda subject: f"In which mythology is {subject} a figure?",
        lambda links: "easy" if links >= 40 else "medium",
    ),
    (
        "creatures",
        "Mythology",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q2239243; wdt:P361 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 3)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 800
        """,
        lambda subject: f"Which tradition tells stories about {subject}?",
        lambda links: "medium" if links >= 20 else "hard",
    ),
    (
        "legislatures",
        "Politics",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q6256; wdt:P194 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 8)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 400
        """,
        lambda subject: f"What is the national legislature of {subject} called?",
        lambda links: "medium",
    ),
    (
        "parties",
        "Politics",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q7278; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 8)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 2000
        """,
        lambda subject: f"In which country is the {subject} a political party?",
        by_links,
    ),
    (
        "governments",
        "Politics",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q6256; wdt:P122 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 10)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 400
        """,
        lambda subject: f"What form of government does {subject} have?",
        lambda links: "medium" if links >= 40 else "hard",
    ),
    (
        "companies",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q4830453; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 18)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 2200
        """,
        lambda subject: f"In which country is the company {subject} based?",
        by_links,
    ),
    (
        "anthems",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q6256; wdt:P85 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 8)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 300
        """,
        lambda subject: f"What is the national anthem of {subject}?",
        lambda links: "medium" if links >= 40 else "hard",
    ),
    (
        "board games",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q131436; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 4)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 800
        """,
        lambda subject: f"Which country is the game {subject} from?",
        lambda links: "easy" if links >= 25 else "medium",
    ),
    (
        "nobel",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          VALUES ?answer { wd:Q38104 wd:Q44585 wd:Q80061 wd:Q37922 wd:Q35637 wd:Q47170 }
          ?item wdt:P166 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 15)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1200
        """,
        lambda subject: f"In which field did {subject} win a Nobel Prize?",
        by_links,
    ),
    (
        "universities",
        "Society & Culture",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q3918; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 10)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 2000
        """,
        lambda subject: f"In which country is {subject}?",
        by_links,
    ),
    (
        "heritage",
        "Society & Culture",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P1435 wd:Q9259; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 8)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1500
        """,
        lambda subject: f"In which country is the World Heritage site {subject}?",
        by_links,
    ),
    (
        "languages",
        "Society & Culture",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q34770; wdt:P279 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 10)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1200
        """,
        lambda subject: f"Which language family does {subject} belong to?",
        lambda links: "medium" if links >= 30 else "hard",
    ),
    (
        "battles",
        "History",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P31 wd:Q178561; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 10)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 1200
        """,
        lambda subject: f"In which present-day country was the battle of {subject} fought?",
        by_links,
    ),
    (
        "inventions",
        "History",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          ?item wdt:P61 ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 25)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 800
        """,
        lambda subject: f"Who is credited with inventing {subject}?",
        by_links,
    ),
]


def report(questions):
    counts = count_cells(questions)
    print(f"Total {len(questions)}", flush=True)
    for bucket in sorted(counts, key=lambda name: (-sum(counts[name].values()), name)):
        cell = counts[bucket]
        print(
            f"  {bucket}: {sum(cell.values())} "
            f"(easy {cell.get('easy', 0)}, medium {cell.get('medium', 0)}, hard {cell.get('hard', 0)})",
            flush=True,
        )


def main():
    questions, seen = dedupe(load_questions())
    before = len(questions)
    questions = trim(questions)
    seen = {normalize(item["question"]) for item in questions}
    print(f"Trimmed {before} questions down to {len(questions)}.", flush=True)
    save_questions(questions)
    remaining = room_left(count_cells(questions))

    for name, bucket, query, question_for, preferred_for in JOBS:
        if sum(remaining.get(bucket, {}).values()) <= 0:
            print(f"Skip {name}: {bucket} is full.", flush=True)
            continue
        print(f"Wikidata: {name}...", flush=True)
        try:
            found = rows(query)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"  skipped {name}: {error}", flush=True)
            continue
        added = add_from_rows(questions, seen, remaining, bucket, found, question_for, preferred_for)
        print(f"  +{added} (database now {len(questions)})", flush=True)
        save_questions(questions)
        time.sleep(1)

    report(questions)


if __name__ == "__main__":
    main()
