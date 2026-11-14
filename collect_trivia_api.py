"""Download multiple-choice questions from The Trivia API.

The questions are CC BY-NC 4.0. This personal offline quiz can keep a copy
as long as the home screen credits https://the-trivia-api.com.
"""

import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DATABASE_FILE = "questions.json"
API_URL = "https://the-trivia-api.com/v2/questions"
USER_AGENT = "Trivianaut/1.0 (personal offline quiz; educational)"
PAUSE_SECONDS = 0.35

CATEGORIES = {
    "arts_and_literature": "Arts & Literature",
    "film_and_tv": "Film & TV",
    "food_and_drink": "Food & Drink",
    "general_knowledge": "General Knowledge",
    "geography": "Geography",
    "history": "History",
    "music": "Music",
    "science": "Science",
    "society_and_culture": "Society & Culture",
    "sport_and_leisure": "Sport & Leisure",
}
DIFFICULTIES = ("easy", "medium", "hard")

last_request = 0


def fetch(url):
    """Download JSON, backing off if the API asks us to slow down."""
    global last_request
    wait = PAUSE_SECONDS - (time.time() - last_request)
    if last_request and wait > 0:
        time.sleep(wait)

    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code == 429:
            print("Rate limit. Waiting.", flush=True)
            time.sleep(5)
            last_request = time.time()
            return fetch(url)
        raise
    last_request = time.time()
    return data


def load_questions():
    with open(DATABASE_FILE, encoding="utf-8") as file:
        return json.load(file)


def save_questions(questions):
    temporary = DATABASE_FILE + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)
        file.write("\n")
    os.replace(temporary, DATABASE_FILE)


def to_record(item):
    if item.get("type") != "text_choice" or item.get("isNiche"):
        return None
    question = item.get("question", {}).get("text", "").strip()
    correct = str(item.get("correctAnswer", "")).strip()
    incorrect = [str(answer).strip() for answer in item.get("incorrectAnswers", [])]
    choices = incorrect + [correct]
    if not question or len(incorrect) != 3 or len(set(choices)) != 4:
        return None
    category = CATEGORIES.get(item.get("category"))
    difficulty = item.get("difficulty")
    if category is None or difficulty not in DIFFICULTIES:
        return None
    return {
        "category": category,
        "difficulty": difficulty,
        "question": question,
        "correct_answer": correct,
        "incorrect_answers": incorrect,
        "source": "The Trivia API",
    }


def add_batch(questions, seen, results):
    added = 0
    for item in results:
        record = to_record(item)
        if record is None or record["question"] in seen:
            continue
        questions.append(record)
        seen.add(record["question"])
        added += 1
    return added


def main():
    questions = load_questions()
    seen = {item["question"] for item in questions}
    print(f"Starting from {len(questions)} saved questions.", flush=True)
    added_total = 0

    for sweep in range(1, 13):
        added_sweep = 0
        for slug in CATEGORIES:
            for difficulty in DIFFICULTIES:
                url = (
                    f"{API_URL}?limit=50&categories={slug}"
                    f"&difficulties={difficulty}"
                )
                try:
                    batch = fetch(url)
                except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
                    print(f"{slug} {difficulty} failed: {error}", flush=True)
                    continue
                added = add_batch(questions, seen, batch)
                added_sweep += added
                added_total += added
        save_questions(questions)
        print(
            f"Sweep {sweep}: +{added_sweep} "
            f"(database now {len(questions)})",
            flush=True,
        )
        if added_sweep < 40:
            break

    print(f"Added {added_total} questions from The Trivia API.", flush=True)
    print(f"The database has {len(questions)} questions.", flush=True)


if __name__ == "__main__":
    main()
