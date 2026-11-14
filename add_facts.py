import json
import os
import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

DATABASE_FILE = "questions.json"
USER_AGENT = "TriviaLearner/1.0 (personal offline quiz; educational)"
PAUSE_SECONDS = 0.6

next_request = 0
request_lock = threading.Lock()


CURATED = [
    {
        "category": "History",
        "difficulty": "easy",
        "question": "Who was the first emperor of a unified China?",
        "correct_answer": "Qin Shi Huang",
        "incorrect_answers": ["Kublai Khan", "Sun Yat-sen", "Wu Zetian"],
        "fact": "Qin Shi Huang founded the Qin dynasty in 221 BCE after conquering the other Warring States. His government standardized Chinese writing, currency, and weights, and he was buried near the Terracotta Army.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "What is the longest river in Africa?",
        "correct_answer": "The Nile",
        "incorrect_answers": ["The Congo", "The Niger", "The Zambezi"],
        "fact": "The Nile flows north from East Africa through the Sahara and into the Mediterranean Sea. At about 6,650 kilometers, it is usually counted as the world's longest river.",
    },
    {
        "category": "Animals",
        "difficulty": "easy",
        "question": "What is the largest living land animal?",
        "correct_answer": "African bush elephant",
        "incorrect_answers": ["White rhinoceros", "Hippopotamus", "Giraffe"],
        "fact": "African bush elephants can stand about 3 meters tall at the shoulder and weigh several thousand kilograms. Their large ears help them shed heat on the savanna.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "The Colosseum stands in which city?",
        "correct_answer": "Rome",
        "incorrect_answers": ["Athens", "Istanbul", "Tunis"],
        "fact": "Rome's Colosseum opened in 80 CE under Emperor Titus. The amphitheater could hold roughly 50,000 spectators for gladiator shows and public games.",
    },
    {
        "category": "History",
        "difficulty": "medium",
        "question": "In which year did the Berlin Wall open?",
        "correct_answer": "1989",
        "incorrect_answers": ["1961", "1979", "1991"],
        "fact": "On the night of November 9, 1989, crowds crossed the Berlin Wall after an East German official said travel rules would be lifted. The wall had divided the city since 1961.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "What is the smallest country in the world by area?",
        "correct_answer": "Vatican City",
        "incorrect_answers": ["Monaco", "San Marino", "Nauru"],
        "fact": "Vatican City covers about 44 hectares inside Rome. It is the seat of the Catholic Church and has been an independent state since the Lateran Treaty of 1929.",
    },
    {
        "category": "Animals",
        "difficulty": "easy",
        "question": "Which is the largest living bird?",
        "correct_answer": "Ostrich",
        "incorrect_answers": ["Emu", "Emperor penguin", "Wandering albatross"],
        "fact": "The common ostrich of Africa can grow about 2.7 meters tall. It cannot fly, but it can run at highway speeds and lays the largest eggs of any living bird.",
    },
    {
        "category": "History",
        "difficulty": "medium",
        "question": "Machu Picchu was built by which civilization?",
        "correct_answer": "The Inca",
        "incorrect_answers": ["The Maya", "The Aztec", "The Olmec"],
        "fact": "The Inca built Machu Picchu in the 15th century on a ridge above Peru's Urubamba River. The estate was brought to worldwide attention by Hiram Bingham's 1911 expedition.",
    },
    {
        "category": "History",
        "difficulty": "easy",
        "question": "Who was the main author of the Declaration of Independence?",
        "correct_answer": "Thomas Jefferson",
        "incorrect_answers": ["Benjamin Franklin", "John Adams", "Alexander Hamilton"],
        "fact": "Thomas Jefferson drafted the Declaration of Independence in 1776 for a committee that also included John Adams and Benjamin Franklin. The Continental Congress adopted it on July 4.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "Which desert is the largest hot desert on Earth?",
        "correct_answer": "The Sahara",
        "incorrect_answers": ["The Gobi", "The Arabian Desert", "The Kalahari"],
        "fact": "The Sahara covers most of North Africa, about 9 million square kilometers. Antarctica is a larger desert, but it is a cold one.",
    },
    {
        "category": "Animals",
        "difficulty": "easy",
        "question": "What is a group of lions called?",
        "correct_answer": "A pride",
        "incorrect_answers": ["A pack", "A herd", "A troop"],
        "fact": "A lion pride is usually made up of related females, their cubs, and a small number of adult males. The lionesses do most of the hunting.",
    },
    {
        "category": "Geography",
        "difficulty": "medium",
        "question": "Timbuktu is in which present-day country?",
        "correct_answer": "Mali",
        "incorrect_answers": ["Morocco", "Nigeria", "Ethiopia"],
        "fact": "Timbuktu, on the edge of the Sahara in Mali, was a great center of trade and Islamic learning under the Mali and Songhai empires.",
    },
    {
        "category": "History",
        "difficulty": "medium",
        "question": "In which year was Magna Carta sealed?",
        "correct_answer": "1215",
        "incorrect_answers": ["1066", "1415", "1492"],
        "fact": "English barons forced King John to seal Magna Carta at Runnymede in 1215. It limited royal power and later became a symbol of the idea that rulers are subject to the law.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "What is the capital of Canada?",
        "correct_answer": "Ottawa",
        "incorrect_answers": ["Toronto", "Montreal", "Vancouver"],
        "fact": "Queen Victoria chose Ottawa as Canada's capital in 1857. It sits on the Ottawa River, between the mainly English-speaking and French-speaking parts of the country.",
    },
    {
        "category": "Animals",
        "difficulty": "medium",
        "question": "Which mammal is the only one that truly flies?",
        "correct_answer": "A bat",
        "incorrect_answers": ["A flying squirrel", "A sugar glider", "A colugo"],
        "fact": "Bats fly by flapping wings made from skin stretched over very long fingers. Flying squirrels, sugar gliders, and colugos can only glide.",
    },
    {
        "category": "History",
        "difficulty": "medium",
        "question": "Angkor Wat was built in which country?",
        "correct_answer": "Cambodia",
        "incorrect_answers": ["Thailand", "Vietnam", "Laos"],
        "fact": "King Suryavarman II built Angkor Wat in the early 12th century as a Hindu temple. It later became a Buddhist monument and is the largest religious structure in the world.",
    },
    {
        "category": "History",
        "difficulty": "medium",
        "question": "Who was the first woman to fly solo across the Atlantic Ocean?",
        "correct_answer": "Amelia Earhart",
        "incorrect_answers": ["Bessie Coleman", "Harriet Quimby", "Amy Johnson"],
        "fact": "Amelia Earhart flew solo from Newfoundland to a pasture in Northern Ireland on May 20–21, 1932. The flight took about 15 hours.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "Which mountain rises highest above sea level?",
        "correct_answer": "Mount Everest",
        "incorrect_answers": ["K2", "Kangchenjunga", "Denali"],
        "fact": "Mount Everest's summit is about 8,849 meters above sea level, on the border of Nepal and China. Edmund Hillary and Tenzing Norgay were the first confirmed climbers to reach the top, in 1953.",
    },
    {
        "category": "Animals",
        "difficulty": "easy",
        "question": "What is a baby kangaroo called?",
        "correct_answer": "A joey",
        "incorrect_answers": ["A cub", "A calf", "A kit"],
        "fact": "A kangaroo joey is born tiny and hairless, then crawls into its mother's pouch. It stays there for months, nursing while it grows.",
    },
    {
        "category": "Geography",
        "difficulty": "medium",
        "question": "The ancient city of Petra is in which country?",
        "correct_answer": "Jordan",
        "incorrect_answers": ["Egypt", "Saudi Arabia", "Israel"],
        "fact": "Petra was the capital of the Nabataean kingdom. Its famous Treasury, Al-Khazneh, is carved into a rose-colored sandstone cliff.",
    },
    {
        "category": "History",
        "difficulty": "easy",
        "question": "In which year did the Titanic sink?",
        "correct_answer": "1912",
        "incorrect_answers": ["1905", "1918", "1923"],
        "fact": "On its first voyage, the Titanic hit an iceberg late on April 14, 1912, and sank in the North Atlantic early the next morning. More than 1,500 people died.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "Which ocean is the largest?",
        "correct_answer": "The Pacific Ocean",
        "incorrect_answers": ["The Atlantic Ocean", "The Indian Ocean", "The Arctic Ocean"],
        "fact": "The Pacific Ocean covers about one third of Earth's surface, from Asia and Australia to the Americas. It is both the largest and the deepest ocean.",
    },
    {
        "category": "Animals",
        "difficulty": "medium",
        "question": "Which big cat is the largest native to the Americas?",
        "correct_answer": "Jaguar",
        "incorrect_answers": ["Cougar", "Ocelot", "Bobcat"],
        "fact": "Jaguars live from Mexico through much of South America. Their bite is strong enough to pierce a turtle's shell, and their spots form broken rings called rosettes.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "What is the capital of Japan?",
        "correct_answer": "Tokyo",
        "incorrect_answers": ["Kyoto", "Osaka", "Hiroshima"],
        "fact": "Tokyo became Japan's capital in 1868, when the emperor moved there from Kyoto. The city was previously known as Edo and was the seat of the Tokugawa shoguns.",
    },
    {
        "category": "History",
        "difficulty": "hard",
        "question": "Who was the leading general of the Haitian Revolution before independence was declared?",
        "correct_answer": "Toussaint Louverture",
        "incorrect_answers": ["Simón Bolívar", "Napoleon Bonaparte", "Henri Christophe"],
        "fact": "The Haitian Revolution began in 1791 with an uprising of enslaved people in the French colony of Saint-Domingue. Toussaint Louverture built the revolutionary army; Jean-Jacques Dessalines declared Haiti independent in 1804.",
    },
    {
        "category": "Animals",
        "difficulty": "medium",
        "question": "How many hearts does an octopus have?",
        "correct_answer": "Three",
        "incorrect_answers": ["One", "Two", "Four"],
        "fact": "An octopus has two hearts that pump blood through the gills and a third that pumps it to the rest of the body. Its blood uses a copper compound and looks blue.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "The Grand Canyon is in which U.S. state?",
        "correct_answer": "Arizona",
        "incorrect_answers": ["Utah", "Colorado", "Nevada"],
        "fact": "The Colorado River carved the Grand Canyon over millions of years. The canyon is about 446 kilometers long, and most of it lies in Grand Canyon National Park.",
    },
    {
        "category": "History",
        "difficulty": "easy",
        "question": "Who was prime minister of the United Kingdom for most of World War II?",
        "correct_answer": "Winston Churchill",
        "incorrect_answers": ["Neville Chamberlain", "Clement Attlee", "David Lloyd George"],
        "fact": "Winston Churchill became prime minister in May 1940, after the German invasion of France, and led Britain until 1945. He served as prime minister again from 1951 to 1955.",
    },
    {
        "category": "Geography",
        "difficulty": "medium",
        "question": "Which country has more lakes than any other?",
        "correct_answer": "Canada",
        "incorrect_answers": ["Russia", "Finland", "The United States"],
        "fact": "Glaciers left Canada with an enormous number of lakes. Counts that include small lakes run into the millions, more than in any other country.",
    },
    {
        "category": "Animals",
        "difficulty": "medium",
        "question": "What is the traditional name for a group of crows?",
        "correct_answer": "A murder",
        "incorrect_answers": ["A parliament", "A gaggle", "An unkindness"],
        "fact": "\"Murder\" is a medieval English collective noun for crows, from the same fashion for fanciful group names that gave us a parliament of owls. An unkindness is the old term for ravens.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "Which of these countries is crossed by the equator?",
        "correct_answer": "Ecuador",
        "incorrect_answers": ["Chile", "Uruguay", "Paraguay"],
        "fact": "Ecuador is named for the equator, which crosses the country. A monument at Mitad del Mundo, near Quito, marks a historic survey of the line.",
    },
    {
        "category": "History",
        "difficulty": "medium",
        "question": "In which century did the Black Death first reach Europe?",
        "correct_answer": "The 14th century",
        "incorrect_answers": ["The 12th century", "The 16th century", "The 18th century"],
        "fact": "The Black Death reached Europe in 1347 and killed a huge part of the population within a few years. The disease was plague, caused by the bacterium Yersinia pestis.",
    },
    {
        "category": "Animals",
        "difficulty": "hard",
        "question": "Which animal has fingerprints remarkably similar to a human's?",
        "correct_answer": "Koala",
        "incorrect_answers": ["Chimpanzee", "Raccoon", "Red panda"],
        "fact": "Koala fingerprints have ridge patterns so close to human ones that they can be difficult to tell apart. Koalas are marsupials native to Australia and live almost entirely on eucalyptus leaves.",
    },
    {
        "category": "Geography",
        "difficulty": "easy",
        "question": "Which city is built on a lagoon and is famous for traveling by canal?",
        "correct_answer": "Venice",
        "incorrect_answers": ["Amsterdam", "Bruges", "Stockholm"],
        "fact": "Venice was built on islands in a shallow lagoon at the north end of the Adriatic Sea. Gondolas and water buses still travel its canals instead of streets.",
    },
    {
        "category": "Geography",
        "difficulty": "medium",
        "question": "What is the largest island in the world?",
        "correct_answer": "Greenland",
        "incorrect_answers": ["New Guinea", "Borneo", "Madagascar"],
        "fact": "Greenland covers about 2.16 million square kilometers, making it the world's largest island. Australia is bigger, but it is counted as a continent rather than an island.",
    },
    {
        "category": "History",
        "difficulty": "easy",
        "question": "Who was the first person to walk on the Moon?",
        "correct_answer": "Neil Armstrong",
        "incorrect_answers": ["Buzz Aldrin", "Yuri Gagarin", "John Glenn"],
        "fact": "Neil Armstrong stepped onto the Moon on July 20, 1969, during Apollo 11. Buzz Aldrin followed him out of the lunar module a few minutes later. Yuri Gagarin was the first person in space, in 1961.",
    },
]


def fetch(url):
    """Download JSON, backing off if Wikipedia asks us to slow down."""
    global next_request
    for attempt in range(6):
        with request_lock:
            wait = next_request - time.time()
            if wait > 0:
                time.sleep(wait)
            next_request = time.time() + PAUSE_SECONDS
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code != 429:
                raise
            time.sleep(5 * (attempt + 1))
        except URLError:
            time.sleep(5 * (attempt + 1))
    raise HTTPError(url, 429, "Too many requests", hdrs=None, fp=None)


def first_sentences(text):
    """Keep a short note, about two sentences."""
    text = re.sub(r"\s+", " ", text).strip()
    pieces = re.split(r"(?<=[.!?])\s+", text)
    kept = []
    total = 0
    for piece in pieces:
        if not piece:
            continue
        if kept and total + len(piece) > 420:
            break
        kept.append(piece)
        total += len(piece) + 1
        if len(kept) == 2:
            break
    return " ".join(kept)


def answer_title(answer):
    """Turn an answer into a likely Wikipedia page title."""
    text = answer.strip().replace("|", " ")
    for prefix in ("The ", "A ", "An "):
        if text.startswith(prefix):
            return text[len(prefix):]
    return text


def usable(extract, answer):
    """Keep a note only when it is substantial and mentions the answer."""
    lowered = extract.lower()
    if len(extract) < 80 or "may refer to" in lowered:
        return False
    words = [word.lower() for word in re.findall(r"[A-Za-z0-9']+", answer) if len(word) > 2]
    if not words:
        return True
    return any(word in lowered for word in words)


def batch_extracts(titles):
    """Ask Wikipedia for the introductions of many pages at once."""
    url = (
        "https://en.wikipedia.org/w/api.php?action=query&prop=extracts"
        "&exintro=1&explaintext=1&redirects=1&format=json&titles="
        + quote("|".join(titles), safe="|")
    )
    data = fetch(url)
    query = data.get("query", {})
    by_title = {}
    for page in query.get("pages", {}).values():
        if "missing" in page:
            continue
        extract = first_sentences(page.get("extract") or "")
        if extract:
            by_title[page["title"].lower()] = extract

    aliases = {}
    for item in query.get("normalized", []):
        aliases[item["from"].lower()] = item["to"].lower()
    for item in query.get("redirects", []):
        aliases[item["from"].lower()] = item["to"].lower()

    found = {}
    for title in titles:
        key = title.lower()
        seen = set()
        while key in aliases and key not in seen:
            seen.add(key)
            key = aliases[key]
        found[title] = by_title.get(key, "")
    return found


def fill_from_titles(questions):
    """Fill facts by looking up each answer as a Wikipedia page title."""
    pending = [item for item in questions if not item.get("fact")]
    found = 0
    for start in range(0, len(pending), 20):
        group = pending[start:start + 20]
        titles = [answer_title(item["correct_answer"]) for item in group]
        extracts = None
        for _ in range(3):
            try:
                extracts = batch_extracts(titles)
                break
            except HTTPError:
                print("Waiting after a rate limit.", flush=True)
                time.sleep(15)
        if extracts is None:
            print("Stopped the title pass because Wikipedia kept rate limiting.", flush=True)
            break
        for item, title in zip(group, titles):
            extract = extracts.get(title, "")
            if usable(extract, item["correct_answer"]):
                item["fact"] = extract
                item["fact_source"] = "Wikipedia"
                found += 1
        done = min(start + 20, len(pending))
        print(f"Title pass {done} of {len(pending)}. Notes: {found}.", flush=True)
        if done % 200 == 0 or done == len(pending):
            save_questions(questions)
    save_questions(questions)
    return found


def lookup_fact(question, answer, category):
    """Find a Wikipedia introduction that is actually about this answer."""
    queries = [
        f"{answer} {category}",
        f"{answer} {question}",
    ]
    for query in queries:
        search_url = (
            "https://en.wikipedia.org/w/api.php?action=query&list=search"
            f"&srsearch={quote(query)}&srlimit=2&maxlag=5&format=json"
        )
        try:
            results = fetch(search_url)["query"]["search"]
        except Exception:
            continue
        for hit in results:
            title = hit["title"]
            extract_url = (
                "https://en.wikipedia.org/w/api.php?action=query&prop=extracts"
                "&exintro=1&explaintext=1&redirects=1&maxlag=5&format=json&titles="
                + quote(title)
            )
            try:
                pages = fetch(extract_url)["query"]["pages"]
            except Exception:
                continue
            extract = first_sentences(next(iter(pages.values())).get("extract", ""))
            lowered = extract.lower()
            if len(extract) < 80 or "may refer to" in lowered or "refer to:" in lowered:
                continue
            answer_words = [word.lower() for word in re.findall(r"[A-Za-z0-9']+", answer) if len(word) > 2]
            if answer_words and not any(word in lowered for word in answer_words):
                continue
            return extract
    return ""


def load_questions():
    with open(DATABASE_FILE, encoding="utf-8") as file:
        return json.load(file)


def save_questions(questions):
    temporary = DATABASE_FILE + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)
        file.write("\n")
    os.replace(temporary, DATABASE_FILE)


def add_curated(questions):
    seen = {item["question"] for item in questions}
    added = 0
    for item in CURATED:
        if item["question"] in seen:
            continue
        questions.append({
            "category": item["category"],
            "difficulty": item["difficulty"],
            "question": item["question"],
            "correct_answer": item["correct_answer"],
            "incorrect_answers": item["incorrect_answers"],
            "source": "original",
            "fact": item["fact"],
            "fact_source": "original",
        })
        seen.add(item["question"])
        added += 1
    return added


def main():
    questions = load_questions()
    added = add_curated(questions)
    save_questions(questions)
    print(f"Added {added} curated questions.", flush=True)

    for item in questions:
        weak = str(item.get("fact", "")).startswith("The correct answer is ")
        if weak and item.get("fact_source") in ("", "answer"):
            item["fact"] = ""
            item["fact_source"] = ""
    print(f"{sum(1 for item in questions if not item.get('fact'))} questions still need a fact.", flush=True)
    found = fill_from_titles(questions)

    needed = [item for item in questions if not item.get("fact")]
    print(f"Searching Wikipedia for the remaining {len(needed)}.", flush=True)
    for index, item in enumerate(needed, start=1):
        try:
            fact = lookup_fact(item["question"], item["correct_answer"], item["category"])
        except HTTPError:
            save_questions(questions)
            print("Wikipedia rate limit persisted. Saved progress and stopped.", flush=True)
            return
        if fact:
            item["fact"] = fact
            item["fact_source"] = "Wikipedia"
            found += 1
        else:
            item["fact"] = f"The correct answer is {item['correct_answer']}."
            item["fact_source"] = "answer"
        if index % 20 == 0:
            save_questions(questions)
            print(f"Search pass {index} of {len(needed)}. Notes: {found}.", flush=True)

    save_questions(questions)
    print(f"Finished. Notes about the answer: {found}. Database size: {len(questions)}.", flush=True)


if __name__ == "__main__":
    main()
