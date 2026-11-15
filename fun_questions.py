"""Add a batch of fun general-knowledge questions and thin out birth years."""

import json
import random
import re

DATABASE_FILE = "questions.json"
KEEP_BIRTH_YEARS = 150
BIRTH_YEAR = re.compile(r"(?:in which year was|what year was|when was).+ born", re.I)

# category, difficulty, question, correct answer, three wrong answers
QUESTIONS = [
    ("General Knowledge", "easy", "How many players from one team are on the field in a standard soccer match?", "11", ["9", "10", "12"]),
    ("General Knowledge", "easy", "In tennis, a score of zero is called what?", "Love", ["Nil", "Blank", "Duck"]),
    ("General Knowledge", "easy", "A perfect score in ten-pin bowling is what?", "300", ["200", "250", "150"]),
    ("General Knowledge", "easy", "How many squares are on a standard chessboard?", "64", ["48", "81", "100"]),
    ("General Knowledge", "easy", "How many pieces does each player start with in chess?", "16", ["12", "18", "20"]),
    ("General Knowledge", "medium", "In a standard U.S. Monopoly set, which dark-blue property is the most expensive on the board?", "Boardwalk", ["Park Place", "Pennsylvania Avenue", "Marvin Gardens"]),
    ("General Knowledge", "easy", "How many strings does a standard guitar have?", "6", ["4", "5", "8"]),
    ("General Knowledge", "easy", "How many keys are on a standard piano?", "88", ["76", "64", "96"]),
    ("General Knowledge", "easy", "How many strings does a standard violin have?", "4", ["5", "6", "3"]),
    ("General Knowledge", "easy", "What color is Mario's cap?", "Red", ["Green", "Blue", "Yellow"]),
    ("General Knowledge", "easy", "What is the name of Mario's brother?", "Luigi", ["Wario", "Toad", "Yoshi"]),
    ("General Knowledge", "easy", "In chess, which piece can jump over other pieces?", "The knight", ["The bishop", "The rook", "The queen"]),
    ("General Knowledge", "easy", "What do the letters in NASA stand for?", "National Aeronautics and Space Administration", ["National Air and Space Agency", "North American Space Association", "National Astronomy and Satellite Agency"]),
    ("General Knowledge", "medium", "The word laser began as an acronym for light amplification by what?", "Stimulated emission of radiation", ["Synchronized energy radiation", "Solar emitted rays", "Sequential electron release"]),
    ("General Knowledge", "easy", "A group of lions is called a what?", "A pride", ["A pack", "A herd", "A flock"]),
    ("General Knowledge", "easy", "A group of crows is called a what?", "A murder", ["A parliament", "A gaggle", "A school"]),
    ("General Knowledge", "medium", "A group of owls is called a what?", "A parliament", ["A murder", "A pride", "A pod"]),
    ("General Knowledge", "easy", "What is a baby kangaroo called?", "A joey", ["A calf", "A cub", "A fawn"]),
    ("General Knowledge", "easy", "What is a baby goat called?", "A kid", ["A foal", "A lamb", "A calf"]),
    ("General Knowledge", "medium", "What is a baby swan called?", "A cygnet", ["A gosling", "A poult", "A fledgling"]),
    ("General Knowledge", "medium", "How many hearts does an octopus have?", "3", ["1", "2", "4"]),
    ("General Knowledge", "medium", "What color is a polar bear's skin?", "Black", ["White", "Pink", "Gray"]),
    ("General Knowledge", "easy", "Flamingos get their pink color mainly from what?", "The food they eat", ["The color of the water", "Sunburn", "Dye painted on at birth"]),
    ("General Knowledge", "easy", "Which metal is a liquid at ordinary room temperature?", "Mercury", ["Iron", "Silver", "Tin"]),
    ("General Knowledge", "easy", "What is the hardest known natural substance?", "Diamond", ["Quartz", "Steel", "Granite"]),
    ("General Knowledge", "easy", "What is the chemical formula for water?", "H2O", ["CO2", "NaCl", "O2"]),
    ("General Knowledge", "easy", "At sea level, water boils at about what temperature?", "100 degrees Celsius", ["90 degrees Celsius", "80 degrees Celsius", "50 degrees Celsius"]),
    ("General Knowledge", "easy", "How many sides does a hexagon have?", "6", ["5", "7", "8"]),
    ("General Knowledge", "easy", "How many colors are in a traditional rainbow?", "7", ["5", "6", "8"]),
    ("General Knowledge", "easy", "How many days are in a leap year?", "366", ["365", "364", "367"]),
    ("General Knowledge", "easy", "In a leap year, February has how many days?", "29", ["28", "30", "31"]),
    ("General Knowledge", "easy", "What is the Roman numeral for 50?", "L", ["C", "D", "V"]),
    ("General Knowledge", "easy", "What is the Roman numeral for 100?", "C", ["L", "M", "X"]),
    ("General Knowledge", "easy", "What is the Roman numeral for 1,000?", "M", ["C", "D", "L"]),
    ("General Knowledge", "easy", "What is the square root of 144?", "12", ["14", "11", "16"]),
    ("General Knowledge", "easy", "Pi is approximately equal to what?", "3.14", ["2.72", "1.62", "4.20"]),
    ("General Knowledge", "easy", "A word that reads the same forward and backward, such as kayak, is called a what?", "A palindrome", ["An anagram", "A homonym", "An acronym"]),
    ("General Knowledge", "medium", "Which language has the most native speakers?", "Mandarin Chinese", ["English", "Spanish", "Hindi"]),
    ("General Knowledge", "easy", "Which ocean is the largest?", "The Pacific Ocean", ["The Atlantic Ocean", "The Indian Ocean", "The Arctic Ocean"]),
    ("General Knowledge", "easy", "Which planet is closest to the Sun?", "Mercury", ["Venus", "Mars", "Earth"]),
    ("General Knowledge", "easy", "Which planet is famous for its bright rings?", "Saturn", ["Jupiter", "Neptune", "Mars"]),
    ("General Knowledge", "easy", "Mount Everest is in which mountain range?", "The Himalayas", ["The Andes", "The Alps", "The Rockies"]),
    ("General Knowledge", "easy", "The Eiffel Tower stands in which city?", "Paris", ["Lyon", "Brussels", "Rome"]),
    ("General Knowledge", "easy", "The Statue of Liberty was a gift to the United States from which country?", "France", ["England", "Spain", "Italy"]),
    ("General Knowledge", "medium", "Big Ben is the nickname of what?", "A bell", ["A clock tower", "A bridge", "A palace"]),
    ("General Knowledge", "easy", "The Colosseum is in which city?", "Rome", ["Athens", "Istanbul", "Madrid"]),
    ("General Knowledge", "easy", "The Great Wall is in which country?", "China", ["Japan", "Mongolia", "India"]),
    ("General Knowledge", "easy", "The Taj Mahal is in which country?", "India", ["Pakistan", "Iran", "Nepal"]),
    ("General Knowledge", "easy", "Machu Picchu is in which country?", "Peru", ["Mexico", "Chile", "Brazil"]),
    ("General Knowledge", "easy", "Which country's flag has a red maple leaf?", "Canada", ["Switzerland", "Japan", "Denmark"]),
    ("General Knowledge", "easy", "Portuguese is the official language of which large South American country?", "Brazil", ["Argentina", "Colombia", "Chile"]),
    ("General Knowledge", "easy", "What is the main ingredient in guacamole?", "Avocado", ["Tomato", "Chickpeas", "Eggplant"]),
    ("General Knowledge", "easy", "Hummus is made mainly from which legume?", "Chickpeas", ["Lentils", "Black beans", "Peas"]),
    ("General Knowledge", "easy", "Traditional pesto is built around which herb?", "Basil", ["Cilantro", "Mint", "Parsley"]),
    ("General Knowledge", "easy", "Which country is most closely associated with paella?", "Spain", ["Italy", "Portugal", "Greece"]),
    ("General Knowledge", "easy", "Pho is a noodle soup from which country?", "Vietnam", ["Thailand", "China", "Korea"]),
    ("General Knowledge", "easy", "Kimchi is a staple food of which country?", "Korea", ["Japan", "China", "Vietnam"]),
    ("General Knowledge", "easy", "Sushi rice is seasoned mainly with what?", "Vinegar", ["Soy sauce", "Honey", "Lime juice"]),
    ("General Knowledge", "medium", "Saffron, the spice, comes from which flower?", "A crocus", ["A rose", "A sunflower", "A lily"]),
    ("General Knowledge", "easy", "Chocolate is made from the seeds of which plant?", "The cacao tree", ["The coffee plant", "The vanilla orchid", "The cola tree"]),
    ("General Knowledge", "easy", "Maple syrup is made by boiling sap from which tree?", "A maple tree", ["An oak tree", "A birch tree", "A pine tree"]),
    ("General Knowledge", "medium", "Tiramisu gets its flavor from which drink?", "Coffee", ["Tea", "Hot chocolate", "Orange juice"]),
    ("General Knowledge", "easy", "A classic s'more is graham cracker, chocolate, and what?", "A marshmallow", ["Peanut butter", "Jam", "Caramel"]),
    ("General Knowledge", "easy", "Haggis is a traditional dish of which country?", "Scotland", ["Ireland", "Wales", "England"]),
    ("General Knowledge", "medium", "Dim sum is a style of meal most associated with which cuisine?", "Chinese", ["Indian", "Mexican", "Ethiopian"]),
    ("General Knowledge", "easy", "Which fruit is the main ingredient in a traditional key lime pie?", "Limes", ["Lemons", "Apples", "Cherries"]),
    ("General Knowledge", "easy", "What are the three primary colors of light?", "Red, green, and blue", ["Red, yellow, and blue", "Cyan, magenta, and yellow", "Orange, green, and purple"]),
    ("General Knowledge", "easy", "How many continents are there in the common seven-continent model?", "7", ["5", "6", "8"]),
    ("General Knowledge", "easy", "What is the smallest continent by land area?", "Australia", ["Europe", "Antarctica", "South America"]),
    ("General Knowledge", "easy", "What is the largest desert in the world, counting polar deserts?", "Antarctica", ["The Sahara", "The Gobi", "The Arabian Desert"]),
    ("General Knowledge", "medium", "Which desert is the largest hot desert?", "The Sahara", ["The Gobi", "The Kalahari", "The Mojave"]),
    ("General Knowledge", "easy", "What do bees make?", "Honey", ["Maple syrup", "Silk", "Wax only"]),
    ("General Knowledge", "easy", "A female deer is called a what?", "A doe", ["A mare", "A hen", "A vixen"]),
    ("General Knowledge", "medium", "A female fox is called a what?", "A vixen", ["A doe", "A jenny", "A pen"]),
    ("General Knowledge", "easy", "How many legs does a spider have?", "8", ["6", "10", "4"]),
    ("General Knowledge", "easy", "How many legs does an insect have?", "6", ["8", "4", "10"]),
    ("General Knowledge", "easy", "What is the largest land animal?", "The African elephant", ["The giraffe", "The hippopotamus", "The rhinoceros"]),
    ("General Knowledge", "easy", "What is the tallest living land animal?", "The giraffe", ["The elephant", "The ostrich", "The moose"]),
    ("General Knowledge", "easy", "Which bird is known for being unable to fly and living in Antarctica?", "The penguin", ["The ostrich", "The kiwi", "The emu"]),
    ("General Knowledge", "easy", "Dolphins and whales belong to which group of animals?", "Mammals", ["Fish", "Reptiles", "Amphibians"]),
    ("General Knowledge", "medium", "A bat is classified as what?", "A mammal", ["A bird", "An insect", "A reptile"]),
    ("General Knowledge", "easy", "What gas do plants take in and use during photosynthesis?", "Carbon dioxide", ["Oxygen", "Nitrogen", "Helium"]),
    ("General Knowledge", "easy", "What force pulls objects toward Earth?", "Gravity", ["Magnetism", "Friction", "Lift"]),
    ("General Knowledge", "easy", "Sound travels fastest through which of these?", "A solid", ["A gas", "A vacuum", "Outer space"]),
    ("General Knowledge", "easy", "Which of these cannot carry sound?", "A vacuum", ["Water", "Steel", "Air"]),
    ("General Knowledge", "easy", "How many stripes are on the United States flag?", "13", ["10", "15", "50"]),
    ("General Knowledge", "easy", "How many stars are on the United States flag?", "50", ["48", "52", "13"]),
    ("General Knowledge", "easy", "Which holiday is celebrated on the Fourth of July in the United States?", "Independence Day", ["Thanksgiving", "Memorial Day", "Labor Day"]),
    ("General Knowledge", "easy", "Halloween falls on which date?", "October 31", ["October 30", "November 1", "September 31"]),
    ("General Knowledge", "easy", "In the Gregorian calendar, which month has exactly 28 days in a common year?", "February", ["April", "June", "November"]),
    ("General Knowledge", "easy", "How many months have 31 days?", "7", ["5", "6", "8"]),
    ("General Knowledge", "medium", "Which month is the only one that can have neither 30 nor 31 days?", "February", ["April", "June", "September"]),
    ("General Knowledge", "easy", "What is the opposite of nocturnal?", "Diurnal", ["Hibernal", "Aquatic", "Arboreal"]),
    ("General Knowledge", "easy", "An animal that eats only plants is called a what?", "A herbivore", ["A carnivore", "An omnivore", "A scavenger"]),
    ("General Knowledge", "easy", "An animal that eats both plants and meat is called a what?", "An omnivore", ["A herbivore", "A carnivore", "A parasite"]),
    ("General Knowledge", "easy", "What is the name of the galaxy that contains our solar system?", "The Milky Way", ["Andromeda", "The Triangulum Galaxy", "The Sombrero Galaxy"]),
    ("General Knowledge", "easy", "How many moons does Earth have?", "1", ["0", "2", "4"]),
    ("General Knowledge", "medium", "Which planet is known as the Red Planet?", "Mars", ["Venus", "Mercury", "Jupiter"]),
    ("General Knowledge", "easy", "What is frozen water called?", "Ice", ["Steam", "Frosting", "Slush only"]),
    ("General Knowledge", "easy", "Water turning into vapor below its boiling point is called what?", "Evaporation", ["Condensation", "Freezing", "Sublimation only"]),
    ("General Knowledge", "medium", "When water vapor turns into liquid droplets, that process is called what?", "Condensation", ["Evaporation", "Melting", "Ionization"]),
    ("General Knowledge", "easy", "Which instrument has black and white keys and is played with the hands?", "The piano", ["The violin", "The trumpet", "The drum"]),
    ("General Knowledge", "easy", "Which brass instrument is bent into a circle and often played in marching bands?", "The sousaphone", ["The flute", "The clarinet", "The violin"]),
    ("General Knowledge", "easy", "A triangle has how many sides?", "3", ["4", "5", "6"]),
    ("General Knowledge", "easy", "A dozen of anything is how many?", "12", ["10", "6", "24"]),
    ("General Knowledge", "easy", "How many items are in a baker's dozen?", "13", ["12", "11", "14"]),
    ("General Knowledge", "easy", "What is 7 times 8?", "56", ["54", "48", "64"]),
    ("General Knowledge", "easy", "How many degrees are in a right angle?", "90", ["45", "180", "360"]),
    ("General Knowledge", "easy", "How many degrees are in a full circle?", "360", ["180", "90", "270"]),
]


def main():
    with open(DATABASE_FILE, encoding="utf-8") as handle:
        questions = json.load(handle)

    births = [item for item in questions if BIRTH_YEAR.search(item["question"])]
    rest = [item for item in questions if not BIRTH_YEAR.search(item["question"])]
    random.Random(21).shuffle(births)
    kept = births[:KEEP_BIRTH_YEARS]
    questions = rest + kept

    seen = {item["question"] for item in questions}
    added = 0
    for category, difficulty, question, correct, wrong in QUESTIONS:
        if question in seen:
            continue
        if len(set([correct, *wrong])) != 4:
            raise SystemExit(f"Duplicate choices: {question}")
        questions.append({
            "category": category,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct,
            "incorrect_answers": list(wrong),
            "source": "original",
        })
        seen.add(question)
        added += 1

    with open(DATABASE_FILE, "w", encoding="utf-8") as handle:
        json.dump(questions, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"Removed {len(births) - len(kept)} birth-year questions.")
    print(f"Added {added} fun questions.")
    print(f"The database now has {len(questions)} questions.")


if __name__ == "__main__":
    main()
