"""Add fun multiple-choice questions from OpenTriviaQA (CC BY-SA 4.0).

Source: https://github.com/uberspot/OpenTriviaQA
Questions that repeat one we already have, or that match the low-quality
filters used on the rest of the bank, are skipped.
"""

import json
import re
import collections
import random
import sys
import urllib.request
from pathlib import Path

from refine_questions import cap_for, junk_reason, shape_of

ROOT = Path(__file__).resolve().parent
SOURCE_NAME = "OpenTriviaQA"
RANDOM = random.Random(11)

# Specific categories are read first so a question keeps its best label
# when the same text also appears in "newest" or "rated".
CATEGORY_MAP = [
    ("movies", "Entertainment: Film", 220),
    ("television", "Entertainment: Television", 160),
    ("music", "Entertainment: Music", 180),
    ("sports", "Sports", 180),
    ("literature", "Entertainment: Books", 100),
    ("history", "History", 140),
    ("science-technology", "Science", 140),
    ("general", "General Knowledge", 180),
    ("entertainment", "Film & TV", 70),
    ("celebrities", "Celebrities", 90),
    ("animals", "Animals", 70),
    ("for-kids", "General Knowledge", 50),
    ("video-games", "Entertainment: Video Games", 60),
    ("people", "Society & Culture", 70),
    ("humanities", "Arts & Literature", 50),
    ("religion-faith", "Mythology", 40),
    ("brain-teasers", "General Knowledge", 30),
    ("geography", "Geography", 30),
    ("hobbies", "Food & Drink", 40),
    ("world", "General Knowledge", 20),
]

BAD_ANSWER = {
    "all of these",
    "none of these",
    "all of the above",
    "none of the above",
    "both",
    "neither",
    "all of them",
    "none of them",
}
BAD_QUESTION = re.compile(
    r"which of (these|the following) statements|"
    r"wrong statement|"
    r"which of the following is true|"
    r"according to .{0,40}(fan site|website|biography)|"
    r"latin name|"
    r"in which of the following states|"
    r"fan site|"
    r"\banatomy of\b|"
    r"\bas of \d{4}|"
    r"\bfirst name of\b|"
    r"\bmiddle name\b|"
    r"\bonly character\b|"
    r"\bmajored?\b|"
    r"\bnominated for\b|"
    r"\bcampus\b|"
    r"\bcoach(?:es|ed|ing)?\b|"
    r"\bretired the jersey\b|"
    r"\bbest friends?\b|"
    r"\buniversity of\b|"
    r"\bepisode\b|"
    r"variety called|"
    r"official bird|"
    r"little league|"
    r"\bmvp\b|"
    r"what do you get when you cross|"
    r"first (?:\w+ ){0,4}(?:player|person|team) to",
    re.I,
)
MOJIBAKE = re.compile(r"Ã.|Â.|â.|�|ï¿½")
POP = re.compile(
    r"\b("
    r"star wars|batman|superman|spider-?man|wonder woman|x-?men|wolverine|avengers|"
    r"harry potter|lord of the rings|hobbit|narnia|disney|pixar|mickey|frozen|"
    r"toy story|wizard of oz|james bond|jurassic|terminator|matrix|godfather|"
    r"titanic|avatar|indiana jones|back to the future|ghostbusters|star trek|"
    r"simpsons|seinfeld|game of thrones|breaking bad|south park|"
    r"beatles|elvis|michael jackson|madonna|rolling stones|nirvana|pink floyd|"
    r"taylor swift|beyonc[eé]|eminem|rihanna|adele|abba|bob dylan|johnny cash|"
    r"david bowie|elton john|"
    r"mario|pokemon|pokémon|zelda|minecraft|nintendo|sonic|pac-?man|"
    r"super bowl|world cup|olympics|wimbledon|stanley cup|world series|"
    r"nba|nfl|mlb|nhl|"
    r"michael jordan|lebron|tiger woods|serena|messi|ronaldo|pele|pelé|"
    r"shakespeare|romeo|hamlet|einstein|newton|darwin|edison|tesla|"
    r"lincoln|washington|kennedy|obama|cleopatra|napoleon|caesar|"
    r"world war|apollo|nasa|moon landing|saturn|jupiter|mars|venus|pluto|"
    r"the moon|the sun|"
    r"rome|greece|egypt|"
    r"oscar|academy award|grammy|hollywood|marvel|pixar|"
    r"mona lisa|van gogh|picasso|beethoven|mozart|bach\b|"
    r"sherlock|dracula|frankenstein|alice in wonderland|peter pan|"
    r"hunger games|twilight|mario kart|pokemon|fortnite"
    r")\b",
    re.I,
)
FAMOUS_YEARS = {
    "1066", "1215", "1492", "1776", "1789", "1812", "1861", "1863", "1865",
    "1912", "1914", "1918", "1929", "1939", "1941", "1944", "1945", "1963",
    "1969", "1989", "2001",
}
MONONYMS = {
    "prince", "madonna", "cher", "beyonce", "beyoncé", "rihanna", "eminem",
    "adele", "drake", "usher", "pink", "sting", "bono", "shakira", "pele",
    "pelé", "plato", "homer", "aristotle", "mozart", "bach", "pele",
}
FOOD = re.compile(
    r"\b(dish|food|cook|recipe|cuisine|soup|bread|cheese|cake|beer|wine|"
    r"coffee|tea|fruit|dessert|pizza|pasta|sandwich|breakfast|dinner|"
    r"drink|cocktail|spice|herb|meat|vegetable|chocolate|ice cream)\b",
    re.I,
)


def norm(text):
    text = text.lower().strip()
    text = text.replace("'", "").replace("'", "")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean(text):
    return re.sub(r"\s+", " ", (text or "").replace("\u00a0", " ")).strip()


def reject(item, category_key):
    question = item.get("question") or ""
    answer = clean(item.get("answer") or "")
    choices = [clean(choice) for choice in item.get("choices") or []]
    if "\n" in question or "\n" in answer:
        return "multiline"
    question = clean(question)
    if not question.endswith("?"):
        return "not a question"
    if not 28 <= len(question) <= 150:
        return "length"
    if MOJIBAKE.search(question) or MOJIBAKE.search(answer) or any(MOJIBAKE.search(c) for c in choices):
        return "encoding"
    if len(choices) != 4 or answer not in choices:
        return "not four choices"
    if len({c.lower() for c in choices}) < 4:
        return "duplicate choices"
    if answer.lower() in BAD_ANSWER or answer.lower().startswith(("all of ", "none of ")):
        return "all of these"
    if any(c.lower() in BAD_ANSWER or c.lower().startswith(("all of ", "none of ")) for c in choices):
        return "all of these"
    if any(len(c) < 1 or len(c) > 42 for c in choices):
        return "choice length"
    if BAD_QUESTION.search(question):
        return "low quality prompt"
    if category_key == "hobbies" and not FOOD.search(question):
        return "not food"
    if category_key == "geography" and not re.search(
        r"\b(country|city|river|mountain|ocean|continent|capital|island|sea|lake|desert|border)\b",
        question,
        re.I,
    ):
        return "not geography"
    record = {
        "category": "General Knowledge",
        "difficulty": "medium",
        "question": question,
        "correct_answer": answer,
        "incorrect_answers": [c for c in choices if c != answer],
        "source": SOURCE_NAME,
    }
    reason = junk_reason(record)
    if reason:
        return reason
    return None


FIXES = {
    "Count Dukoo": "Count Dooku",
    "Southhampton, England": "Southampton, England",
    "Peter, Paul Mary": "Peter, Paul and Mary",
}


def fun_score(question, answer):
    text = question.lower()
    score = 1 if len(question) <= 110 else 0
    if POP.search(question) or POP.search(answer):
        score += 4
    if POP.search(answer):
        score += 2
    if re.search(r"\b(who played|who sang|who wrote|real name|which planet|which band)\b", text):
        score += 2
    if re.search(r"\bnot (a|an)\b|\bis not\b", text):
        score -= 3
    if re.search(r"\b(19|20)\d{2}\b", question) and answer.strip() not in FAMOUS_YEARS:
        score -= 2
    if re.search(r"\b(what|which) year\b|\bin (what|which) year\b", text):
        if answer.strip() not in FAMOUS_YEARS:
            score -= 5
    if re.search(r"\b(died|death|cause of|passed away)\b", text):
        score -= 4
    if re.search(r"\bhow many\b", text) and not re.fullmatch(r"\d{1,3}", answer.strip()):
        score -= 4
    if re.match(r"who\b", text) and " " not in answer.strip() and answer.strip().lower() not in MONONYMS:
        score -= 5
    return score


def better_category(question, category):
    text = question.lower()
    if category in {"Science", "History", "Geography", "Sports", "Society & Culture", "General Knowledge"} and re.search(
        r"\b(movie|film|sitcom|tv show|actor|actress)\b", text
    ):
        return "Film & TV"
    if category == "Science" and re.search(r"\b(super bowl|world cup|olympics|nba|nfl)\b", text):
        return "Sports"
    return category


def main():
    apply = "--apply" in sys.argv
    bank = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))
    download = ROOT / "_otqa.json"
    if not download.exists():
        request = urllib.request.Request(
            "https://raw.githubusercontent.com/uberspot/OpenTriviaQA/master/util/CategorisedQuestionList.json",
            headers={"User-Agent": "trivia-scraper"},
        )
        download.write_bytes(urllib.request.urlopen(request, timeout=120).read())
    incoming = json.loads(download.read_text(encoding="utf-8"))
    seen = {norm(q["question"]) for q in bank}
    shapes = collections.Counter(shape_of(q["question"]) for q in bank)
    added_by = collections.Counter()
    rejected = collections.Counter()
    chosen = []
    used_norms = set()

    for key, category, limit in CATEGORY_MAP:
        items = incoming.get(key) or []
        pool = []
        for raw in items:
            item = {
                "question": clean(raw.get("question") or "").replace("diety", "deity"),
                "answer": FIXES.get(clean(raw.get("answer") or ""), clean(raw.get("answer") or "")),
                "choices": [FIXES.get(clean(choice), clean(choice)) for choice in raw.get("choices") or []],
            }
            reason = reject(item, key)
            if reason:
                rejected[reason] += 1
                continue
            question = clean(item["question"])
            answer = clean(item["answer"])
            key_norm = norm(question)
            if key_norm in seen or key_norm in used_norms:
                rejected["repeat"] += 1
                continue
            shape = shape_of(question)
            if shapes[shape] >= cap_for(shape):
                rejected["repeated wording"] += 1
                continue
            score = fun_score(question, answer)
            if score < 5:
                rejected["not widely known"] += 1
                continue
            choices = [FIXES.get(clean(choice), clean(choice)) for choice in item["choices"]]
            answer = FIXES.get(answer, answer)
            pool.append((score, RANDOM.random(), {
                "category": better_category(question, category),
                "difficulty": "medium",
                "question": question,
                "correct_answer": answer,
                "incorrect_answers": [choice for choice in choices if choice != answer],
                "source": SOURCE_NAME,
            }, shape, key_norm))
        pool.sort(key=lambda row: (row[0], row[1]), reverse=True)
        picked = []
        for score, _tie, record, shape, key_norm in pool:
            if shapes[shape] >= cap_for(shape) or key_norm in used_norms:
                continue
            picked.append(record)
            used_norms.add(key_norm)
            shapes[shape] += 1
            if len(picked) >= limit:
                break
        chosen.extend(picked)
        added_by[category] += len(picked)
        print(f"{key:20} kept {len(picked):4} / cap {limit}")

    print(f"\nnew questions {len(chosen)}")
    print("rejected", sum(rejected.values()))
    for reason, count in rejected.most_common(12):
        print(f"  {count:6}  {reason}")
    print("\nadded by category:")
    for name, count in added_by.most_common():
        print(f"  {count:4}  {name}")

    print("\n--- by category ---")
    grouped = collections.defaultdict(list)
    for record in chosen:
        grouped[record["category"]].append(record)
    for name in ("Entertainment: Film", "Entertainment: Music", "Sports", "Science", "History", "General Knowledge"):
        print(f"\n# {name}")
        rows = grouped[name][:]
        RANDOM.shuffle(rows)
        for record in rows[:6]:
            print(f"- {record['question']}")
            print(f"    => {record['correct_answer']}")

    print("\n--- samples ---")
    sample = chosen[:]
    RANDOM.shuffle(sample)
    for record in sample[:24]:
        print(f"- {record['question']}")
        print(f"    => {record['correct_answer']}  [{record['category']}]")

    if apply:
        bank.extend(chosen)
        temporary = ROOT / "questions.json.tmp"
        temporary.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(ROOT / "questions.json")
        print(f"\nwrote questions.json ({len(bank)} questions)")


if __name__ == "__main__":
    main()
