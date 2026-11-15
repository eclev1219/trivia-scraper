"""Fill the categories that are still short of the balanced targets.

Queries are kept small so Wikidata does not time out. Facts are public
Wikidata data. The question wording is written here.
"""

import time

import balance_database as db

ONE_SHOTS = [
    (
        "animal groups",
        "Animals",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {
          VALUES ?answer { wd:Q7377 wd:Q5113 wd:Q10811 wd:Q152 wd:Q10908 }
          ?item wdt:P31 wd:Q16521; wdt:P105 wd:Q7432; wdt:P171* ?answer; wikibase:sitelinks ?links.
          FILTER(?links > 25)
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 800
        """,
        lambda subject: f"The {subject.lower()} belongs to which animal group?",
        db.by_links,
    ),
]

SLICES = [
    (
        "deity religions",
        "Mythology",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q178885; wdt:P140 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 500
        """,
        lambda subject: f"Which tradition is {subject} associated with?",
        db.by_links,
    ),
    (
        "creature lands",
        "Mythology",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q2239243; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 400
        """,
        lambda subject: f"Which country are stories of {subject} most associated with?",
        lambda links: "medium" if links >= 20 else "hard",
    ),
    (
        "writers",
        "Arts & Literature",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P106 wd:Q36180; wdt:P27 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 450
        """,
        lambda subject: f"Which country is the writer {subject} from?",
        db.by_links,
    ),
    (
        "books",
        "Arts & Literature",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q7725634; wdt:P50 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 400
        """,
        lambda subject: f"Who wrote {subject}?",
        db.by_links,
    ),
    (
        "ships",
        "Vehicles",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q11446; wdt:P137 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 400
        """,
        lambda subject: f"Which operator is associated with the ship {subject}?",
        lambda links: "medium" if links >= 25 else "hard",
    ),
    (
        "drinks",
        "Food & Drink",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P279 wd:Q40050; wdt:P495 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 400
        """,
        lambda subject: f"Which country is {subject} associated with?",
        lambda links: "easy" if links >= 20 else "medium",
    ),
    (
        "more parties",
        "Politics",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q7278; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 500
        """,
        lambda subject: f"In which country is the {subject} a political party?",
        db.by_links,
    ),
    (
        "more companies",
        "General Knowledge",
        """
        SELECT ?itemLabel ?answerLabel ?links WHERE {{
          ?item wdt:P31 wd:Q4830453; wdt:P17 ?answer; wikibase:sitelinks ?links.
          FILTER({link_filter})
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT 500
        """,
        lambda subject: f"In which country is the company {subject} based?",
        db.by_links,
    ),
]

LINK_RANGES = (
    "?links >= 80",
    "?links >= 40 && ?links < 80",
    "?links >= 20 && ?links < 40",
    "?links >= 8 && ?links < 20",
)


def main():
    questions = db.load_questions()
    seen = {db.normalize(item["question"]) for item in questions}
    print(f"Starting from {len(questions)} questions.", flush=True)

    for name, bucket, query, question_for, preferred_for in ONE_SHOTS:
        remaining = db.room_left(db.count_cells(questions))
        if sum(remaining.get(bucket, {}).values()) <= 0:
            continue
        print(f"{name}...", flush=True)
        try:
            found = db.rows(query)
        except Exception as error:
            print(f"  skipped: {error}", flush=True)
            continue
        before = len(questions)
        db.add_from_rows(questions, seen, remaining, bucket, found, question_for, preferred_for)
        print(f"  +{len(questions) - before} (database now {len(questions)})", flush=True)
        db.save_questions(questions)

    for name, bucket, template, question_for, preferred_for in SLICES:
        for link_filter in LINK_RANGES:
            remaining = db.room_left(db.count_cells(questions))
            if bucket != "General Knowledge" and sum(remaining.get(bucket, {}).values()) <= 0:
                break
            if len(questions) >= 28000 and bucket == "General Knowledge":
                break
            print(f"{name} ({link_filter})...", flush=True)
            try:
                found = db.rows(template.format(link_filter=link_filter))
            except Exception as error:
                print(f"  skipped: {error}", flush=True)
                continue
            before = len(questions)
            if bucket == "General Knowledge" and sum(remaining["General Knowledge"].values()) <= 0:
                # Keep general knowledge ahead, up to 5,500, once the base cap is full.
                for difficulty in db.DIFFICULTIES:
                    remaining["General Knowledge"][difficulty] += 700
            db.add_from_rows(questions, seen, remaining, bucket, found, question_for, preferred_for)
            print(f"  +{len(questions) - before} (database now {len(questions)})", flush=True)
            db.save_questions(questions)
            time.sleep(0.8)
            if len(questions) >= 28500:
                db.report(questions)
                return

    db.report(questions)


if __name__ == "__main__":
    main()
