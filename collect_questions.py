import html
import json
import os
import time
from urllib.request import urlopen

DATABASE_FILE = "questions.json"
CATEGORY_URL = "https://opentdb.com/api_category.php"
TOKEN_URL = "https://opentdb.com/api_token.php?command=request"
API_URL = "https://opentdb.com/api.php"
PAUSE_SECONDS = 5.2

# The time of the last web request. Open Trivia DB allows one request every 5 seconds.
last_request = 0


def clean(text):
    """Turn encoded characters such as &quot; back into normal text."""
    return html.unescape(text).strip()


def fetch(url):
    """Download one JSON document, waiting so requests stay 5 seconds apart."""
    global last_request
    wait = PAUSE_SECONDS - (time.time() - last_request)
    if last_request and wait > 0:
        time.sleep(wait)

    with urlopen(url, timeout=30) as response:
        data = json.load(response)
    last_request = time.time()
    return data


def to_record(item):
    """Keep one multiple-choice question, or None if it does not have four choices."""
    incorrect = [clean(answer) for answer in item["incorrect_answers"]]
    correct = clean(item["correct_answer"])
    choices = incorrect + [correct]
    if len(incorrect) != 3 or len(set(choices)) != 4:
        return None

    return {
        "category": clean(item["category"]),
        "difficulty": item["difficulty"],
        "question": clean(item["question"]),
        "correct_answer": correct,
        "incorrect_answers": incorrect,
        "source": "Open Trivia DB",
        "fact": "",
        "fact_source": "",
    }


def load_existing():
    try:
        with open(DATABASE_FILE, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_questions(questions):
    """Replace the database only after the new file is fully written."""
    temporary = DATABASE_FILE + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)
        file.write("\n")
    os.replace(temporary, DATABASE_FILE)


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


def collect_category(token, category, questions, seen):
    """Download every multiple-choice question in one category."""
    amount = 50
    empty_replies = 0
    added = 0

    while True:
        url = (
            f"{API_URL}?amount={amount}&category={category['id']}"
            f"&type=multiple&token={token}"
        )
        data = fetch(url)
        code = data["response_code"]

        if code == 0:
            new_questions = add_batch(questions, seen, data["results"])
            added += new_questions
            save_questions(questions)
            print(
                f"{category['name']}: +{new_questions} "
                f"(database now {len(questions)})",
                flush=True,
            )
            amount = 50
            empty_replies = 0
            continue

        if code == 5:
            print("Rate limit. Waiting before the next request.", flush=True)
            continue

        if code == 1 and amount > 1:
            amount = max(1, amount // 2)
            continue

        if code == 4:
            empty_replies += 1
            if empty_replies < 2:
                continue
            return added

        print(f"{category['name']} stopped with code {code}.", flush=True)
        return added


def main():
    questions = load_existing()
    seen = {item["question"] for item in questions}
    print(f"Starting from {len(questions)} saved questions.", flush=True)

    categories = fetch(CATEGORY_URL)["trivia_categories"]
    token = fetch(TOKEN_URL)["token"]

    for category in categories:
        collect_category(token, category, questions, seen)

    print(f"Finished. The database has {len(questions)} questions.", flush=True)


if __name__ == "__main__":
    main()
