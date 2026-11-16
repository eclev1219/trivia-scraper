ROWS = []

def put(cat, diff, q, a, b, c, d):
    ROWS.append((cat, diff, q, a, b, c, d))

def wrongs(pool, answer):
    out = []
    for item in pool:
        if item != answer and item not in out:
            out.append(item)
        if len(out) == 3:
            return out
    raise SystemExit(answer)

caps = [
("Czechia", "Prague"), ("Hungary", "Budapest"), ("Romania", "Bucharest"),
("Ukraine", "Kyiv"), ("Croatia", "Zagreb"), ("Serbia", "Belgrade"),
("Bulgaria", "Sofia"), ("Morocco", "Rabat"), ("Algeria", "Algiers"),
("Tunisia", "Tunis"), ("Ghana", "Accra"), ("Ethiopia", "Addis Ababa"),
("Tanzania", "Dodoma"), ("Uganda", "Kampala"), ("Senegal", "Dakar"),
("Iran", "Tehran"), ("Iraq", "Baghdad"), ("The United Arab Emirates", "Abu Dhabi"),
("Qatar", "Doha"), ("Jordan", "Amman"), ("Lebanon", "Beirut"),
("Pakistan", "Islamabad"), ("Bangladesh", "Dhaka"), ("Nepal", "Kathmandu"),
("Mongolia", "Ulaanbaatar"), ("Malaysia", "Kuala Lumpur"),
("Singapore", "Singapore"), ("Cambodia", "Phnom Penh"), ("Laos", "Vientiane"),
("Costa Rica", "San Jose"), ("Panama", "Panama City"),
("Jamaica", "Kingston"), ("Uruguay", "Montevideo"), ("Paraguay", "Asuncion"),
("Ecuador", "Quito"), ("Venezuela", "Caracas"), ("Cuba", "Havana"),
("Wales", "Cardiff"), ("Scotland", "Edinburgh"),
]
# Singapore as country and city makes the answer appear... city Singapore is the answer, question says Singapore. Skip those where answer is inside the country name.
cities = [c for _, c in caps]
for country, city in caps:
    if city.lower() in country.lower():
        continue
    put("Geography", "medium", f"This city is the capital of {country}.", city, *wrongs(cities, city))

zodiac = [
("March 21 to April 19", "Aries"), ("April 20 to May 20", "Taurus"),
("May 21 to June 20", "Gemini"), ("June 21 to July 22", "Cancer"),
("July 23 to August 22", "Leo"), ("August 23 to September 22", "Virgo"),
("September 23 to October 22", "Libra"), ("October 23 to November 21", "Scorpio"),
("November 22 to December 21", "Sagittarius"), ("December 22 to January 19", "Capricorn"),
("January 20 to February 18", "Aquarius"), ("February 19 to March 20", "Pisces"),
]
signs = [s for _, s in zodiac]
for dates, sign in zodiac:
    put("General Knowledge", "medium", f"People born {dates} have this zodiac sign.", sign, *wrongs(signs, sign))

notes = ["A", "B", "C", "D", "E", "F", "G"]
# skip, too thin

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
days = {
"January": "31", "February": "28", "March": "31", "April": "30", "May": "31", "June": "30",
"July": "31", "August": "31", "September": "30", "October": "31", "November": "30", "December": "31",
}
dayvals = ["28", "30", "31", "29"]
for month, count in days.items():
    w = [d for d in dayvals if d != count][:3]
    put("General Knowledge", "easy", f"In a common year, {month} has this many days.", count, *w)

sports = [
("This team plays home games at Lambeau Field.", "The Green Bay Packers", "The Chicago Bears", "The Detroit Lions", "The Minnesota Vikings", "medium"),
("This team plays home games at Fenway Park.", "The Boston Red Sox", "The New York Yankees", "The Chicago Cubs", "The Los Angeles Dodgers", "easy"),
("This team plays home games at Wrigley Field.", "The Chicago Cubs", "The Chicago White Sox", "The St. Louis Cardinals", "The Milwaukee Brewers", "medium"),
("This team plays home games at Yankee Stadium.", "The New York Yankees", "The New York Mets", "The Boston Red Sox", "The Philadelphia Phillies", "easy"),
("This basketball team is nicknamed the Lakers.", "Los Angeles", "Boston", "Chicago", "Miami", "easy"),
("This basketball team is nicknamed the Celtics.", "Boston", "New York", "Philadelphia", "Chicago", "easy"),
("This football team is nicknamed the Cowboys.", "Dallas", "Houston", "Denver", "Kansas City", "easy"),
("This football team is nicknamed the Packers.", "Green Bay", "Chicago", "Minnesota", "Detroit", "easy"),
("This soccer club is nicknamed the Red Devils.", "Manchester United", "Liverpool", "Arsenal", "Chelsea", "medium"),
("This soccer club plays at Camp Nou.", "Barcelona", "Real Madrid", "Atletico Madrid", "Sevilla", "medium"),
("This soccer club plays at Santiago Bernabeu.", "Real Madrid", "Barcelona", "Valencia", "Bayern Munich", "medium"),
("This tennis tournament is played at Flushing Meadows.", "The U.S. Open", "Wimbledon", "The French Open", "The Australian Open", "medium"),
("This tennis tournament is played at Roland-Garros.", "The French Open", "Wimbledon", "The U.S. Open", "The Australian Open", "medium"),
("This golf major is played at Augusta National.", "The Masters", "The U.S. Open", "The Open Championship", "The PGA Championship", "easy"),
("A grand slam in tennis means winning all four of these in one year.", "The majors", "The World Cup", "The Olympics", "The Davis Cup only", "medium"),
("This swimmer won 23 Olympic gold medals.", "Michael Phelps", "Mark Spitz", "Katie Ledecky", "Caeleb Dressel", "medium"),
("This gymnast is known for huge medals totals in the 2010s and 2020s.", "Simone Biles", "Nadia Comaneci", "Shawn Johnson", "Aly Raisman", "easy"),
("This tennis player has the most Grand Slam singles titles in the men's Open Era.", "Novak Djokovic", "Roger Federer", "Rafael Nadal", "Pete Sampras", "hard"),
("This tennis player won 22 Grand Slam singles titles.", "Rafael Nadal", "Roger Federer", "Novak Djokovic", "Andy Murray", "hard"),
("This country has won the most Olympic medals overall.", "The United States", "China", "Russia", "Great Britain", "medium"),
]
for q, a, b, c, d, diff in sports:
    put("Sports", diff, q, a, b, c, d)

# Djokovic has the most now (24). Nadal has 22. Federer 20. The question "most in open era" is Djokovic. The "22 slams" is Nadal. Good.
# "Davis Cup only" is a weak distractor. Change if I can.

films = [
("This 1993 film follows dinosaurs in a theme park.", "Jurassic Park", "The Lost World", "King Kong", "Godzilla", "easy"),
("This 1999 film asks you to choose the red pill.", "The Matrix", "The Matrix Reloaded", "Inception", "Dark City", "easy"),
("This 1985 film sends a teen back to 1955.", "Back to the Future", "Peggy Sue Got Married", "Back to the Future Part II", "Weird Science", "easy"),
("This 1975 film made people afraid of the ocean.", "Jaws", "Orca", "The Deep", "Piranha", "easy"),
("This 1939 film follows a girl to the Emerald City.", "The Wizard of Oz", "The Wiz", "Return to Oz", "Wicked", "easy"),
("This 1965 film features a nanny with a flying umbrella.", "Mary Poppins", "Chitty Chitty Bang Bang", "Bedknobs and Broomsticks", "The Sound of Music", "medium"),
("This 1965 film is about a singing family fleeing Austria.", "The Sound of Music", "Mary Poppins", "My Fair Lady", "Fiddler on the Roof", "medium"),
("This 1959 film is an epic about a chariot race in Rome.", "Ben-Hur", "Spartacus", "Gladiator", "Quo Vadis", "hard"),
("This 1960 film is Hitchcock's famous shower scene.", "Psycho", "Vertigo", "The Birds", "Rear Window", "medium"),
("This 1954 film follows dockworkers and a pigeon coop.", "On the Waterfront", "Rebel Without a Cause", "East of Eden", "A Streetcar Named Desire", "hard"),
("This 1942 film is set in a cafe in wartime Morocco.", "Casablanca", "The Maltese Falcon", "To Have and Have Not", "Key Largo", "medium"),
("This 1972 crime film is about the Corleone family.", "The Godfather", "The Godfather Part II", "Goodfellas", "Scarface", "easy"),
("This 1990 gangster film follows Henry Hill.", "Goodfellas", "Casino", "The Irishman", "Donnie Brasco", "medium"),
("This 1983 film is about a drug lord in Miami.", "Scarface", "Carlito's Way", "Blow", "Traffic", "medium"),
("This 2019 film follows a family living in a basement.", "Parasite", "Snowpiercer", "The Host", "Okja", "medium"),
("This 2023 film follows the man who led the atomic bomb project.", "Oppenheimer", "Barbie", "Maestro", "The Imitation Game", "easy"),
("This 2010 film explores dreams inside dreams.", "Inception", "Interstellar", "Tenet", "The Prestige", "easy"),
("This 2014 film sends explorers through a wormhole.", "Interstellar", "Gravity", "The Martian", "Arrival", "medium"),
("This 2015 film strands an astronaut on Mars.", "The Martian", "Interstellar", "Gravity", "Ad Astra", "medium"),
("This 2016 musical follows jazz musicians in Los Angeles.", "La La Land", "Whiplash", "The Artist", "Chicago", "medium"),
]
for q, a, b, c, d, diff in films:
    put("Entertainment: Film", diff, q, a, b, c, d)

books = [
("This poet wrote The Raven.", "Edgar Allan Poe", "Walt Whitman", "Emily Dickinson", "Robert Frost", "medium"),
("This poet wrote Leaves of Grass.", "Walt Whitman", "Edgar Allan Poe", "Emily Dickinson", "Henry Wadsworth Longfellow", "hard"),
("This poet wrote Because I could not stop for Death.", "Emily Dickinson", "Walt Whitman", "Sylvia Plath", "Maya Angelou", "hard"),
("This author wrote The Odyssey.", "Homer", "Virgil", "Sophocles", "Ovid", "medium"),
("This author wrote The Aeneid.", "Virgil", "Homer", "Ovid", "Horace", "hard"),
("This playwright wrote Oedipus Rex.", "Sophocles", "Euripides", "Aeschylus", "Aristophanes", "hard"),
("This author wrote Don Quixote.", "Miguel de Cervantes", "Lope de Vega", "Gabriel Garcia Marquez", "Jorge Luis Borges", "medium"),
("This author wrote One Hundred Years of Solitude.", "Gabriel Garcia Marquez", "Isabel Allende", "Julio Cortazar", "Mario Vargas Llosa", "hard"),
("This author wrote Crime and Punishment.", "Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Ivan Turgenev", "medium"),
("This author wrote War and Peace.", "Leo Tolstoy", "Fyodor Dostoevsky", "Alexander Pushkin", "Nikolai Gogol", "medium"),
("This author wrote The Little Prince.", "Antoine de Saint-Exupery", "Jules Verne", "Victor Hugo", "Albert Camus", "medium"),
("This author wrote Les Miserables.", "Victor Hugo", "Alexandre Dumas", "Honore de Balzac", "Gustave Flaubert", "medium"),
("This author wrote The Three Musketeers.", "Alexandre Dumas", "Victor Hugo", "Jules Verne", "Emile Zola", "easy"),
("This author wrote Around the World in Eighty Days.", "Jules Verne", "H.G. Wells", "Alexandre Dumas", "Robert Louis Stevenson", "medium"),
("This author wrote Treasure Island.", "Robert Louis Stevenson", "Jules Verne", "Daniel Defoe", "Jonathan Swift", "medium"),
("This author wrote Robinson Crusoe.", "Daniel Defoe", "Jonathan Swift", "Robert Louis Stevenson", "Herman Melville", "medium"),
("This author wrote Gulliver's Travels.", "Jonathan Swift", "Daniel Defoe", "Voltaire", "Laurence Sterne", "medium"),
("This author wrote The Divine Comedy.", "Dante Alighieri", "Petrarch", "Boccaccio", "Virgil", "medium"),
("This author wrote The Canterbury Tales.", "Geoffrey Chaucer", "William Shakespeare", "John Milton", "Edmund Spenser", "hard"),
("This author wrote Paradise Lost.", "John Milton", "John Donne", "William Blake", "Geoffrey Chaucer", "hard"),
]
for q, a, b, c, d, diff in books:
    put("Entertainment: Books", diff, q, a, b, c, d)

science = [
("This planet has the Great Red Spot.", "Jupiter", "Saturn", "Neptune", "Mars", "easy"),
("This planet's day is longer than its year.", "Venus", "Mercury", "Mars", "Earth", "hard"),
("This is the only planet known to support life.", "Earth", "Mars", "Venus", "Europa", "easy"),
("This dwarf planet was reclassified in 2006.", "Pluto", "Ceres", "Eris", "Haumea", "easy"),
("This is the main gas in Earth's atmosphere.", "Nitrogen", "Oxygen", "Carbon dioxide", "Argon", "medium"),
("This gas makes up about 21 percent of Earth's air.", "Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen", "medium"),
("This metal is liquid at room temperature.", "Mercury", "Gallium", "Lead", "Sodium", "medium"),
("This is the lightest element.", "Hydrogen", "Helium", "Lithium", "Oxygen", "easy"),
("Diamonds are a form of this element.", "Carbon", "Silicon", "Quartz", "Calcium", "medium"),
("Table salt contains sodium and this element.", "Chlorine", "Iodine", "Fluorine", "Bromine", "medium"),
("This vitamin is produced in skin exposed to sunlight.", "Vitamin D", "Vitamin C", "Vitamin A", "Vitamin K", "medium"),
("This vitamin is famous for preventing scurvy.", "Vitamin C", "Vitamin D", "Vitamin B12", "Vitamin E", "medium"),
("This part of the eye controls how much light enters.", "The pupil", "The retina", "The lens", "The iris", "medium"),
("This part of the eye focuses light.", "The lens", "The retina", "The cornea", "The pupil", "hard"),
("This part of the eye detects light.", "The retina", "The lens", "The iris", "The pupil", "medium"),
]
for q, a, b, c, d, diff in science:
    put("Science", diff, q, a, b, c, d)

# iris controls light more than pupil. The pupil is the hole. "controls how much light" is the iris. Fix.
for i, row in enumerate(ROWS):
    if row[2].startswith("This part of the eye controls"):
        ROWS[i] = ("Science", "medium", "This part of the eye is the colored ring that controls light.", "The iris", "The pupil", "The lens", "The retina")

food = [
("This spice is the dried stigma of a crocus.", "Saffron", "Turmeric", "Paprika", "Annatto", "hard"),
("This hot pepper is the base of sriracha's heat.", "Chili", "Black pepper", "Horseradish", "Mustard", "medium"),
("Wasabi served with sushi is traditionally this plant.", "Horseradish relative", "Chili", "Ginger", "Radish", "hard"),
("This Japanese condiment is pickled ginger.", "Gari", "Wasabi", "Nori", "Miso", "hard"),
("This bread is traditionally unleavened and used at Passover.", "Matzo", "Challah", "Pita", "Naan", "medium"),
("This braided bread is served on Shabbat.", "Challah", "Matzo", "Rye", "Focaccia", "medium"),
("This French bread is long and crusty.", "A baguette", "A brioche", "A croissant", "A baguette's cousin pain de mie", "easy"),
("This flaky French pastry is crescent shaped.", "A croissant", "A danish", "A scone", "A bagel", "easy"),
("This boiled bread with a hole is a New York staple.", "A bagel", "A pretzel", "A donut", "A biscuit", "easy"),
("This twisted salted snack is often sold at ballparks.", "A pretzel", "A bagel", "A churro", "A breadstick", "easy"),
]
for q, a, b, c, d, diff in food:
    put("Food & Drink", diff, q, a, b, c, d)

# Fix awkward wrong answers
for i, row in enumerate(ROWS):
    if "pain de mie" in row[5] or "pain de mie" in row[6]:
        ROWS[i] = ("Food & Drink", "easy", "This French bread is long and crusty.", "A baguette", "A brioche", "A croissant", "Ciabatta")
    if row[3] == "Horseradish relative":
        ROWS[i] = ("Food & Drink", "hard", "Real wasabi comes from a plant in this family.", "The horseradish family", "The chili family", "The ginger family", "The mint family")
    if row[2].startswith("This hot pepper is the base of sriracha"):
        ROWS[i] = ("Food & Drink", "medium", "Sriracha gets its heat from this kind of pepper.", "Chili peppers", "Black pepper", "Bell peppers", "Banana peppers")
