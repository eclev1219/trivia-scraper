import json
import random

DATABASE_FILE = "questions.json"


def load_questions():
    """Read the saved question list."""
    try:
        with open(DATABASE_FILE, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise SystemExit("No database yet. Run: python build_database.py")


def filter_questions(questions, difficulty=None, category=None):
    """Keep questions that match the chosen difficulty and category.

    None means "all", so that filter is skipped.
    """
    chosen = []
    for question in questions:
        if difficulty is not None and question["difficulty"] != difficulty:
            continue
        if category is not None and question["category"] != category:
            continue
        chosen.append(question)
    return chosen


def unique_sorted(questions, field):
    """Return each different value of one field, in alphabetical order."""
    names = []
    for question in questions:
        if question[field] not in names:
            names.append(question[field])
    names.sort()
    return names


def choose_from_menu(title, options):
    """Show numbered choices. Each option is a (label, value) pair."""
    print()
    print(title)
    for index, (label, value) in enumerate(options):
        print(f"  {index}. {label}")

    while True:
        typed = input("Choose a number: ").strip()
        if typed.isdigit():
            number = int(typed)
            if 0 <= number < len(options):
                return options[number][1]
        print(f"Type a number from 0 to {len(options) - 1}.")


def choose_round(questions):
    """Ask for a difficulty and a category, then return the matching questions."""
    while True:
        difficulty_options = [("All", None)]
        for name in ("easy", "medium", "hard"):
            count = len(filter_questions(questions, difficulty=name))
            difficulty_options.append((f"{name} ({count})", name))
        difficulty = choose_from_menu("Difficulty", difficulty_options)

        pool = filter_questions(questions, difficulty=difficulty)
        category_options = [(f"All ({len(pool)})", None)]
        for name in unique_sorted(pool, "category"):
            count = len(filter_questions(pool, category=name))
            category_options.append((f"{name} ({count})", name))
        category = choose_from_menu("Category", category_options)

        chosen = filter_questions(pool, category=category)
        if chosen:
            return chosen
        print("No questions match that combination. Try again.")


def choose_how_many(available):
    """Ask how many questions to play, and keep asking until the number is valid."""
    while True:
        typed = input(f"How many questions? (1-{available}): ").strip()
        if typed.isdigit():
            count = int(typed)
            if 1 <= count <= available:
                return count
        print(f"Type a whole number from 1 to {available}.")


def ask(question, number, total):
    """Show one question with four shuffled choices. Return True if the user is correct."""
    choices = [question["correct_answer"], *question["incorrect_answers"]]
    random.shuffle(choices)

    print(f"Question {number} of {total}")
    print(f"{question['category']} ({question['difficulty']})")
    print(question["question"])
    print()
    for index, choice in enumerate(choices, start=1):
        print(f"  {index}. {choice}")
    print()

    while True:
        typed = input("Your answer (1-4, or q to stop): ").strip().lower()
        if typed == "q":
            return None
        if typed in {"1", "2", "3", "4"}:
            picked = choices[int(typed) - 1]
            break
        print("Type 1, 2, 3, 4, or q.")

    if picked == question["correct_answer"]:
        print("Correct.")
        return True

    print("The answer was:", question["correct_answer"])
    return False


def main():
    questions = load_questions()
    round_questions = choose_round(questions)
    random.shuffle(round_questions)
    count = choose_how_many(len(round_questions))
    round_questions = round_questions[:count]

    score = 0
    answered = 0
    for number, question in enumerate(round_questions, start=1):
        print()
        result = ask(question, number, count)
        if result is None:
            break
        answered += 1
        if result:
            score += 1
        print(f"Score: {score} / {answered}")

    print()
    print(f"Final score: {score} / {answered}")


main()
