import html
import json
from urllib.request import urlopen

# Open Trivia DB gives us questions as data. amount=5 means "send 5 questions".
API_URL = "https://opentdb.com/api.php?amount=5&type=multiple"


def fetch_questions():
    """Download questions and turn the response into Python data."""
    with urlopen(API_URL) as response:
        data = json.load(response)
    return data["results"]


def show_question(item):
    """Print one question and its correct answer."""
    question = html.unescape(item["question"])
    answer = html.unescape(item["correct_answer"])
    print(question)
    print("Answer:", answer)
    print()


def main():
    questions = fetch_questions()
    for item in questions:
        show_question(item)


main()
