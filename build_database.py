import html
import json
from urllib.request import urlopen

# amount=50 is the most questions Open Trivia DB will send in one request.
API_URL = "https://opentdb.com/api.php?amount=50&type=multiple"
DATABASE_FILE = "questions.json"


def clean(text):
    """Turn encoded characters such as &quot; back into normal text."""
    return html.unescape(text)


def fetch_questions():
    """Download one batch of questions."""
    with urlopen(API_URL) as response:
        data = json.load(response)

    # 0 means the request worked. Any other code means we did not get questions.
    if data["response_code"] != 0:
        raise SystemExit(f"Open Trivia DB returned code {data['response_code']}")

    return data["results"]


def to_record(item):
    """Keep the fields the quiz needs, with readable text."""
    incorrect = [clean(answer) for answer in item["incorrect_answers"]]
    if len(incorrect) != 3:
        return None

    return {
        "category": clean(item["category"]),
        "difficulty": item["difficulty"],
        "question": clean(item["question"]),
        "correct_answer": clean(item["correct_answer"]),
        "incorrect_answers": incorrect,
    }


def load_existing():
    """Read the database, or start from an empty list if it does not exist yet."""
    try:
        with open(DATABASE_FILE, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def add_new(existing, fresh):
    """Add questions whose text is not already in the database."""
    seen = {item["question"] for item in existing}
    added = 0
    for item in fresh:
        if item["question"] in seen:
            continue
        existing.append(item)
        seen.add(item["question"])
        added += 1
    return added


def save_questions(questions):
    """Write the whole list to questions.json."""
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)


def main():
    raw_questions = fetch_questions()
    fresh = []
    for item in raw_questions:
        record = to_record(item)
        if record is not None:
            fresh.append(record)

    questions = load_existing()
    added = add_new(questions, fresh)
    save_questions(questions)
    print(f"Added {added} new questions.")
    print(f"The database now has {len(questions)} questions in {DATABASE_FILE}.")


main()
