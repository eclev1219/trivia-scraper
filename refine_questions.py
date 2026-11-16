"""Drop low-quality, copy-pasted trivia and keep questions an average player can enjoy."""

import json
import re
import collections
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RANDOM = random.Random(7)

FAMOUS = [
    "united states", "united kingdom", "england", "scotland", "ireland", "wales",
    "france", "japan", "italy", "spain", "germany", "china", "canada", "australia",
    "mexico", "brazil", "india", "russia", "egypt", "greece", "netherlands",
    "portugal", "sweden", "norway", "south korea", "argentina", "south africa",
    "turkey", "poland", "switzerland", "austria", "belgium", "denmark",
    "new zealand", "israel", "cuba", "thailand", "finland", "iceland",
    "paris", "london", "rome", "tokyo", "berlin", "madrid", "moscow", "beijing",
    "cairo", "athens", "dublin", "venice", "florence", "barcelona", "amsterdam",
    "vienna", "prague", "istanbul", "jerusalem", "mecca", "hollywood",
    "new york", "los angeles", "chicago", "washington", "boston", "seattle",
    "sydney", "toronto", "ottawa", "hawaii", "alaska", "texas", "california",
    "versailles", "eiffel", "forbidden city", "big ben", "statue of liberty",
    "niagara", "grand canyon", "machu picchu", "colosseum", "coliseum", "kremlin",
    "pyramids", "stonehenge", "great wall", "taj mahal", "louvre", "vatican",
    "disneyland", "mount rushmore", "golden gate", "sydney opera", "everest",
    "kilimanjaro", "amazon", "sahara", "nile", "mississippi", "thames",
    "mediterranean", "caribbean", "victoria falls", "great barrier",
    "hollywood", "las vegas", "times square", "buckingham", "white house",
    "pentagon", "notre dame", "sistine", "acropolis", "pompeii", "atlantis",
    "pizza", "sushi", "hamburger", "taco", "croissant", "pretzel", "paella",
    "pasta", "chocolate", "coffee", "champagne", "whiskey", "whisky", "vodka",
    "tequila", "bagel", "hot dog", "barbecue", "curry", "ramen", "pho",
    "baguette", "fondue", "goulash", "tiramisu", "gelato", "maple syrup",
    "soccer", "football", "basketball", "baseball", "tennis", "cricket",
    "golf", "hockey", "olympics", "karate", "judo", "taekwondo", "tae kwon",
    "samba", "tango", "jazz", "reggae", "ballet", "opera",
    "christmas", "halloween", "thanksgiving",
    "shakespeare", "beatles", "disney", "pixar", "mario", "pokemon", "zelda",
    "star wars", "harry potter", "lord of the rings", "marvel", "batman",
    "superman", "spider-man", "spiderman", "mickey mouse", "elvis", "madonna",
    "michael jackson", "beyonce", "taylor swift",
]

AUTHORS = [
    "shakespeare", "dickens", "tolkien", "rowling", "austen", "orwell", "twain",
    "doyle", "poe", "shelley", "stoker", "hemingway", "fitzgerald", "steinbeck",
    "dahl", "seuss", "andersen", "grimm", "homer", "dante", "plato", "aristotle",
    "voltaire", "hugo", "dumas", "verne", "christie", "stephen king", "dan brown",
    "pratchett", "c.s. lewis", "c. s. lewis", "lewis carroll", "barrie", "milne",
    "wilde", "kafka", "tolstoy", "dostoevsky", "dostoyevsky", "cervantes",
    "melville", "hawthorne", "alcott", "bronte", "brontë", "wells", "stevenson",
    "kipling", "baum", "collodi", "defoe", "swift", "chaucer", "milton",
    "bradbury", "asimov", "gaiman", "salinger",
    "vonnegut", "golding", "carroll", "potter", "atwood",
    "morrison", "angelou", "woolf", "hemingway", "steinbeck",
    "grisham", "crichton", "clancy", "riordan", "collins", "meyer",
    "saint-exup", "saint exup", "coelho", "achebe", "dickinson", "frost",
    "whitman", "hughes", "miller", "beckett", "shaw", "moliere", "molière",
    "goethe", "nietzsche", "aesop", "sun tzu", "machiavelli", "confucius",
    "virgil", "sophocles", "ovid", "chekhov", "pushkin", "garcia marquez",
    "garcía márquez", "allende", "murakami", "le guin", "philip k. dick",
    "phillip k. dick", "bradbury", "verne", "christie", "agatha",
    "j.k. rowling", "j. k. rowling", "dr. seuss", "roald", "george orwell",
    "mark twain", "jane austen", "harper lee", "f. scott", "ernest",
    "mary shelley", "bram stoker", "jules verne", "victor hugo",
    "hans christian", "brothers grimm", "l. frank baum", "beatrix potter",
    "e.b. white", "e. b. white", "margaret atwood", "maya angelou",
    "toni morrison", "neil gaiman", "terry pratchett", "douglas adams",
    "frank herbert", "isaac asimov", "ray bradbury", "h.g. wells", "h. g. wells",
    "robert louis", "louisa may", "charles dickens", "william shakespeare",
    "oscar wilde", "edgar allan", "emily bront", "charlotte bront",
    "fyodor", "leo tolstoy", "alexandre dumas", "arthur conan doyle",
    "george r.r. martin", "george r. r. martin", "suzanne collins",
    "stephenie meyer", "stephanie meyer", "rick riordan", "john grisham",
    "michael crichton", "tom clancy", "j.d. salinger", "j. d. salinger",
    "kurt vonnegut", "joseph heller", "william golding", "george bernard shaw",
    "antoine de saint",
]

OLOGIES = {
    "biology", "geology", "astronomy", "psychology", "archaeology", "archeology",
    "ecology", "zoology", "botany", "cardiology", "dermatology", "etymology",
    "meteorology", "paleontology", "seismology", "ornithology", "entomology",
    "anthropology", "sociology", "criminology", "pharmacology", "neurology",
    "pathology", "oncology", "toxicology", "oceanography", "genealogy",
    "herpetology", "audiology", "ophthalmology", "cosmology", "astrology",
    "microbiology", "physiology", "theology", "mythology",
}

PLACE_Q = re.compile(
    r"\b(which|what) country\b"
    r"|\bwhere (is|was|are|were|did|would|in the world|can)\b"
    r"|\bin which country\b"
    r"|\bcapital(?: city)? of\b"
    r"|\bcity in which country\b"
    r"|\bwhich continent\b",
    re.I,
)
TOURNAMENT = re.compile(
    r"world cup|olympics|olympic games|super bowl|stanley cup|wimbledon|"
    r"world series|champions league|grand prix|tour de france|the ashes|"
    r"euro 20|uefa|nba finals|world championship",
    re.I,
)
ORIGIN = re.compile(
    r"\bendemic\b|\bnative to\b|\boriginat|\boriginally\b|\bcomes? from\b|"
    r"country of origin|\bfrom which country\b|"
    r"which country is .{0,90}\bfrom\b|"
    r"what country .{0,50}\b(from|originate)\b|"
    r"\bborn\b|"
    r"associated with|"
    r"\bbased in\b",
    re.I,
)
JUNK = [
    (re.compile(r"political party", re.I), "political party"),
    (re.compile(r"present-day country|battle of the battle|was the battle", re.I), "battle location"),
    (re.compile(r"which company (makes|built|manufactures|produced)", re.I), "which company makes"),
    (re.compile(r"operator is associated with the ship", re.I), "ship operator"),
    (re.compile(r"chemical symbol", re.I), "chemical symbol"),
    (re.compile(r"national legislature|form of government|official currency|official language", re.I), "civics template"),
    (re.compile(r"nobel prize", re.I), "nobel template"),
    (re.compile(r"language family", re.I), "language family"),
    (re.compile(r"web address|top-level domain|\btld\b", re.I), "domain ending"),
    (re.compile(r"dog breed", re.I), "dog breed origin"),
    (re.compile(r"team based in", re.I), "local team"),
    (re.compile(r"nickname of the .{0,30}(football|soccer) team", re.I), "club nickname"),
    (re.compile(r"flag can be described", re.I), "flag description"),
    (re.compile(r"which of these (people|artists|authors|writers|composers|players|men|women) is not", re.I), "nationality odd one out"),
    (re.compile(r"\bdiploid\b|\bluminous intensity\b|\bmolecular formula\b|\batomic mass\b", re.I), "textbook detail"),
    (re.compile(r"which of these countries borders|countries border|country borders", re.I), "bordering country"),
    (re.compile(r"unit of currency|\bcurrency\b", re.I), "currency"),
    (re.compile(r"in which year was .{0,80} born|\bborn in which\b", re.I), "birth year"),
    (re.compile(r"https?://|wikidata|\bgenid\b", re.I), "wiki junk"),
]
BAD_ANSWER = re.compile(r"https?://|wikidata|\bgenid\b|^Q\d+$|various authors", re.I)


def mentions(text, phrases):
    low = text.lower()
    for phrase in phrases:
        if re.search(r"\b" + re.escape(phrase) + r"\b", low):
            return True
    return False


def shape_of(question):
    text = question.strip().replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    text = re.sub(r'"[^"]{0,80}"', " TITLE ", text)
    text = re.sub(r"'[^']{0,80}'", " TITLE ", text)
    text = re.sub(r"\b\d[\d,]*(?:st|nd|rd|th)?\b", " N ", text, flags=re.I)
    words = text.split()
    out = []
    for index, word in enumerate(words):
        bare = re.sub(r"^[^\w]+|[^\w]+$", "", word)
        if index > 0 and bare[:1].isupper() and bare.lower() not in {"i"}:
            out.append("§")
        else:
            out.append(word)
    collapsed = re.sub(r"(?:§\s+)+", "§ ", " ".join(out))
    collapsed = re.sub(r"\s+", " ", collapsed).strip().lower()
    return re.sub(r"[?.!]+$", "", collapsed)


def has_name(question):
    return "§" in shape_of(question)


def cap_for(shape):
    if "author wrote" in shape or shape.startswith("who wrote"):
        return 12
    if "capital" in shape:
        return 16
    if "study of" in shape:
        return 12
    if "world cup" in shape or "olympics" in shape:
        return 10
    if "stand for" in shape:
        return 12
    if "phonetic" in shape:
        return 6
    if "group of" in shape or "collective noun" in shape or "young " in shape:
        return 8
    if "flag of" in shape:
        return 8
    return 7


def source_score(question):
    return {
        "original": 100,
        "Open Trivia DB": 70,
        "The Trivia API": 45,
        None: 30,
        "SciQ": 8,
        "Wikidata": 0,
    }.get(question.get("source"), 20)


def score(question):
    value = source_score(question)
    value -= min(len(question["question"]), 220) / 25
    if mentions(question["correct_answer"], AUTHORS) or mentions(question["question"], FAMOUS):
        value += 20
    return value


def junk_reason(question):
    text = question["question"]
    answer = question.get("correct_answer") or ""
    choices = question.get("incorrect_answers") or []
    if not text or not answer or len(choices) < 3:
        return "incomplete"
    if len({answer.strip().lower(), *(c.strip().lower() for c in choices)}) < 4:
        return "duplicate choices"
    if BAD_ANSWER.search(answer) or any(BAD_ANSWER.search(c or "") for c in choices):
        return "junk answer"
    if len(text) > 200:
        return "overlong prompt"
    if question.get("source") == "SciQ" and (len(text) > 115 or not text.strip().endswith("?")):
        return "textbook wording"
    for pattern, reason in JUNK:
        if pattern.search(text) or pattern.search(answer):
            return reason
    if re.search(r"\bthe study of\b", text, re.I):
        if not any(re.search(r"\b" + name + r"\b", text, re.I) for name in OLOGIES):
            return "obscure field of study"
    if question.get("source") == "Wikidata":
        if re.search(r"\bwrote\b", text, re.I) and mentions(answer, AUTHORS):
            return None
        return "wikidata template"
    if PLACE_Q.search(text) and not TOURNAMENT.search(text):
        if re.search(r"\bcapital(?: city)? of\b", text, re.I):
            if not mentions(text, FAMOUS):
                return "obscure capital"
        elif ORIGIN.search(text) and not mentions(text, FAMOUS):
            return "where is it from"
        elif has_name(text) and not mentions(text, FAMOUS):
            return "where is it from"
    if re.search(r"\bflag of\b", text, re.I) and not mentions(text, FAMOUS):
        return "obscure flag"
    if re.search(r"\b(which author wrote|who wrote|who is the author)\b", text, re.I):
        if not mentions(answer, AUTHORS) and not mentions(text, FAMOUS):
            return "obscure author"
    return None


def main():
    apply = "--apply" in sys.argv
    questions = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))
    reasons = collections.Counter()
    kept = []
    for question in questions:
        reason = junk_reason(question)
        if reason:
            reasons[reason] += 1
            continue
        kept.append(question)

    by_shape = collections.defaultdict(list)
    for question in kept:
        by_shape[shape_of(question["question"])].append(question)

    capped_ids = set()
    for shape, group in by_shape.items():
        limit = cap_for(shape)
        if len(group) <= limit:
            continue
        ranked = sorted(group, key=score, reverse=True)
        chosen = []
        per_answer = collections.Counter()
        for question in ranked:
            answer = question["correct_answer"].strip().lower()
            if per_answer[answer] >= 2:
                continue
            chosen.append(id(question))
            per_answer[answer] += 1
            if len(chosen) >= limit:
                break
        for question in group:
            if id(question) not in chosen:
                capped_ids.add(id(question))
    reasons["repeated wording"] = len(capped_ids)
    kept = [question for question in kept if id(question) not in capped_ids]

    print(f"before {len(questions)}")
    print(f"after  {len(kept)}")
    print(f"removed {len(questions) - len(kept)}")
    print("\nremoved by reason:")
    for reason, count in reasons.most_common():
        print(f"  {count:5}  {reason}")
    print("\nkept by category:")
    for name, count in collections.Counter(q["category"] for q in kept).most_common():
        print(f"  {count:5}  {name}")
    print("\nkept by source:")
    for name, count in collections.Counter(q.get("source") for q in kept).most_common():
        print(f"  {count:5}  {name}")
    print("\ntop remaining shapes:")
    shapes = collections.Counter(shape_of(q["question"]) for q in kept)
    for shape, count in shapes.most_common(20):
        print(f"  {count:4}  {shape[:110]}")

    place_left = [q for q in kept if PLACE_Q.search(q["question"]) and not TOURNAMENT.search(q["question"])]
    print(f"\nplace questions still in the bank: {len(place_left)}")
    for question in place_left[:25]:
        print(f"  ? {question['question'][:120]} => {question['correct_answer'][:40]}")

    print("\n--- sample kept ---")
    sample = kept[:]
    RANDOM.shuffle(sample)
    for question in sample[:30]:
        print(f"- {question['question'][:130]}")
        print(f"    => {question['correct_answer'][:60]}  [{question['category']}]")

    if apply:
        (ROOT / "questions.json").write_text(
            json.dumps(kept, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("\nwrote questions.json")


if __name__ == "__main__":
    main()
