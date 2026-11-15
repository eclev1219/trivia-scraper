"""Add a last batch so the database clears 25,000 questions.

These are new wordings of public Wikidata facts, mostly general knowledge.
"""

import balance_database as db

JOBS = [
    (
        "headquarters",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q4830453; wdt:P159 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 600
        """,
        lambda subject: f"In which city is {subject} headquartered?",
        db.by_links,
    ),
    (
        "founders",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q4830453; wdt:P112 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 500
        """,
        lambda subject: f"Who founded {subject}?",
        lambda links: "medium" if links >= 30 else "hard",
    ),
    (
        "cheeses",
        "Food & Drink",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P279 wd:Q10943; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 400
        """,
        lambda subject: f"Which country is {subject} from?",
        lambda links: "easy" if links >= 15 else "medium",
    ),
    (
        "cat breeds",
        "Animals",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q43577; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 300
        """,
        lambda subject: f"Which country is the {subject} cat breed associated with?",
        lambda links: "medium",
    ),
]

RANGES = (
    "?links >= 40",
    "?links >= 15 && ?links < 40",
    "?links >= 5 && ?links < 15",
)


def main():
    questions = db.load_questions()
    seen = {db.normalize(item["question"]) for item in questions}
    print(f"Starting from {len(questions)} questions.", flush=True)
    for name, bucket, template, question_for, preferred_for in JOBS:
        for link_filter in RANGES:
            if len(questions) >= 27000:
                db.report(questions)
                return
            remaining = db.room_left(db.count_cells(questions))
            if bucket == "General Knowledge":
                for difficulty in db.DIFFICULTIES:
                    remaining[bucket][difficulty] += 800
            elif sum(remaining.get(bucket, {}).values()) <= 0:
                break
            print(f"{name} ({link_filter})...", flush=True)
            try:
                found = db.rows(template.format(link_filter=link_filter))
            except Exception as error:
                print(f"  skipped: {error}", flush=True)
                continue
            before = len(questions)
            db.add_from_rows(questions, seen, remaining, bucket, found, question_for, preferred_for)
            print(f"  +{len(questions) - before} (database now {len(questions)})", flush=True)
            db.save_questions(questions)
    db.report(questions)


if __name__ == "__main__":
    main()
