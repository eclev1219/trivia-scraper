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
    return out

nfl = [
("Arizona Cardinals", "Glendale"), ("Atlanta Falcons", "Atlanta"),
("Baltimore Ravens", "Baltimore"), ("Buffalo Bills", "Orchard Park"),
("Carolina Panthers", "Charlotte"), ("Chicago Bears", "Chicago"),
("Cincinnati Bengals", "Cincinnati"), ("Cleveland Browns", "Cleveland"),
("Dallas Cowboys", "Arlington"), ("Denver Broncos", "Denver"),
("Detroit Lions", "Detroit"), ("Green Bay Packers", "Green Bay"),
("Houston Texans", "Houston"), ("Indianapolis Colts", "Indianapolis"),
("Jacksonville Jaguars", "Jacksonville"), ("Kansas City Chiefs", "Kansas City"),
("Las Vegas Raiders", "Las Vegas"), ("Los Angeles Chargers", "Inglewood"),
("Los Angeles Rams", "Inglewood"), ("Miami Dolphins", "Miami Gardens"),
("Minnesota Vikings", "Minneapolis"), ("New England Patriots", "Foxborough"),
("New Orleans Saints", "New Orleans"), ("New York Giants", "East Rutherford"),
("New York Jets", "East Rutherford"), ("Philadelphia Eagles", "Philadelphia"),
("Pittsburgh Steelers", "Pittsburgh"), ("San Francisco 49ers", "Santa Clara"),
("Seattle Seahawks", "Seattle"), ("Tampa Bay Buccaneers", "Tampa"),
("Tennessee Titans", "Nashville"), ("Washington Commanders", "Landover"),
]
cities = []
for _, c in nfl:
    if c not in cities:
        cities.append(c)
for team, city in nfl:
    put("Sports", "medium", f"The {team} play their home games in this area.", city, *wrongs(cities, city))

nba = [
("Boston Celtics", "Boston"), ("Brooklyn Nets", "Brooklyn"),
("New York Knicks", "New York"), ("Philadelphia 76ers", "Philadelphia"),
("Toronto Raptors", "Toronto"), ("Chicago Bulls", "Chicago"),
("Cleveland Cavaliers", "Cleveland"), ("Detroit Pistons", "Detroit"),
("Indiana Pacers", "Indianapolis"), ("Milwaukee Bucks", "Milwaukee"),
("Atlanta Hawks", "Atlanta"), ("Charlotte Hornets", "Charlotte"),
("Miami Heat", "Miami"), ("Orlando Magic", "Orlando"),
("Washington Wizards", "Washington"), ("Denver Nuggets", "Denver"),
("Minnesota Timberwolves", "Minneapolis"), ("Oklahoma City Thunder", "Oklahoma City"),
("Portland Trail Blazers", "Portland"), ("Utah Jazz", "Salt Lake City"),
("Golden State Warriors", "San Francisco"), ("Los Angeles Clippers", "Inglewood"),
("Los Angeles Lakers", "Los Angeles"), ("Phoenix Suns", "Phoenix"),
("Sacramento Kings", "Sacramento"), ("Dallas Mavericks", "Dallas"),
("Houston Rockets", "Houston"), ("Memphis Grizzlies", "Memphis"),
("New Orleans Pelicans", "New Orleans"), ("San Antonio Spurs", "San Antonio"),
]
nc = []
for _, c in nba:
    if c not in nc:
        nc.append(c)
for team, city in nba:
    put("Sports", "medium", f"The {team} are based in this city.", city, *wrongs(nc, city))

presidents = [
(1, "George Washington", "easy"), (3, "Thomas Jefferson", "easy"),
(16, "Abraham Lincoln", "easy"), (18, "Ulysses S. Grant", "medium"),
(26, "Theodore Roosevelt", "medium"), (32, "Franklin D. Roosevelt", "easy"),
(34, "Dwight D. Eisenhower", "medium"), (35, "John F. Kennedy", "easy"),
(36, "Lyndon B. Johnson", "medium"), (37, "Richard Nixon", "easy"),
(40, "Ronald Reagan", "easy"), (42, "Bill Clinton", "easy"),
(43, "George W. Bush", "easy"), (44, "Barack Obama", "easy"),
(45, "Donald Trump", "easy"), (46, "Joe Biden", "easy"),
]
pnames = [n for _, n, _ in presidents]
for num, name, diff in presidents:
    put("History", diff, f"This person was the {num}th president of the United States." if num not in (1, 3) else f"This person was president number {num} of the United States.", name, *wrongs(pnames, name))

quotes = [
("May the Force be with you", "Star Wars", ("Star Trek", "Dune", "The Matrix"), "easy"),
("Here's looking at you, kid", "Casablanca", ("Gone with the Wind", "Citizen Kane", "The Maltese Falcon"), "medium"),
("I'll be back", "The Terminator", ("Predator", "RoboCop", "Total Recall"), "easy"),
("You can't handle the truth", "A Few Good Men", ("The Firm", "Jerry Maguire", "A Time to Kill"), "medium"),
("To infinity and beyond", "Toy Story", ("Lightyear", "Buzz Lightyear of Star Command", "Cars"), "easy"),
("Just keep swimming", "Finding Nemo", ("Finding Dory", "Moana", "The Little Mermaid"), "easy"),
("I see dead people", "The Sixth Sense", ("The Others", "Ghost", "Stir of Echoes"), "medium"),
("Here's Johnny", "The Shining", ("Misery", "Carrie", "It"), "medium"),
("You talking to me", "Taxi Driver", ("Raging Bull", "Goodfellas", "Scarface"), "hard"),
("I am your father", "Star Wars", ("Star Trek", "Dune", "Superman"), "easy"),
("Life is like a box of chocolates", "Forrest Gump", ("Big", "Cast Away", "The Terminal"), "easy"),
("Why so serious", "The Dark Knight", ("Joker", "Batman Begins", "The Batman"), "easy"),
("I feel the need for speed", "Top Gun", ("Days of Thunder", "Top Gun: Maverick", "Iron Eagle"), "medium"),
("Nobody puts Baby in a corner", "Dirty Dancing", ("Footloose", "Grease", "Flashdance"), "medium"),
("You're gonna need a bigger boat", "Jaws", ("The Meg", "Deep Blue Sea", "Titanic"), "easy"),
]
for line, film, w, diff in quotes:
    put("Entertainment: Film", diff, f"The line '{line}' comes from this film.", film, *w)

directors2 = [
("Spirited Away", "Hayao Miyazaki", ("Isao Takahata", "Makoto Shinkai", "Satoshi Kon")),
("My Neighbor Totoro", "Hayao Miyazaki", ("Isao Takahata", "Mamoru Hosoda", "Hideaki Anno")),
("Your Name", "Makoto Shinkai", ("Hayao Miyazaki", "Mamoru Hosoda", "Satoshi Kon")),
("Psycho", "Alfred Hitchcock", ("Orson Welles", "Billy Wilder", "Stanley Kubrick")),
("Vertigo", "Alfred Hitchcock", ("Orson Welles", "Roman Polanski", "Brian De Palma")),
("2001: A Space Odyssey", "Stanley Kubrick", ("Ridley Scott", "Steven Spielberg", "George Lucas")),
("The Shining", "Stanley Kubrick", ("Brian De Palma", "John Carpenter", "David Cronenberg")),
("Alien", "Ridley Scott", ("James Cameron", "John Carpenter", "David Fincher")),
("Blade Runner", "Ridley Scott", ("Denis Villeneuve", "James Cameron", "George Lucas")),
("Mad Max: Fury Road", "George Miller", ("Ridley Scott", "James Cameron", "Christopher Nolan")),
("Parasite", "Bong Joon-ho", ("Park Chan-wook", "Hirokazu Kore-eda", "Lee Chang-dong")),
("Everything Everywhere All at Once", "Daniel Kwan and Daniel Scheinert", ("The Wachowskis", "Christopher Nolan", "Greta Gerwig")),
("Get Out", "Jordan Peele", ("Jordan Peele's brother", "Spike Lee", "Boots Riley")),
]
for film, director, w in directors2:
    if "brother" in w[0]:
        w = ("Spike Lee", "Boots Riley", "Ari Aster")
    put("Entertainment: Film", "hard", f"This director made {film}.", director, *w)

science2 = [
("Photosynthesis mainly happens in this plant part.", "Leaves", "Roots", "Flowers", "Bark", "easy"),
("This pigment makes leaves green.", "Chlorophyll", "Carotene", "Melanin", "Hemoglobin", "medium"),
("This gas do plants release during photosynthesis.", "Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen", "easy"),
("The boiling point of water in Fahrenheit is this.", "212", "100", "180", "32", "easy"),
("The freezing point of water in Fahrenheit is this.", "32", "0", "212", "100", "easy"),
("This planet has a giant red spot.", "Jupiter", "Saturn", "Neptune", "Mars", "medium"),
("This planet rotates on its side.", "Uranus", "Neptune", "Venus", "Saturn", "hard"),
("This planet is named for the Roman god of war.", "Mars", "Jupiter", "Mercury", "Saturn", "medium"),
("This planet is named for the Roman messenger god.", "Mercury", "Mars", "Venus", "Neptune", "medium"),
("Sound cannot travel through this.", "A vacuum", "Water", "Steel", "Air", "medium"),
("This is the center of the solar system.", "The Sun", "Earth", "Jupiter", "The Moon", "easy"),
("This is Earth's natural satellite.", "The Moon", "Phobos", "Titan", "Europa", "easy"),
("A lunar eclipse happens when Earth blocks light from reaching this.", "The Moon", "The Sun", "Mars", "Venus", "medium"),
("A solar eclipse happens when this blocks the Sun.", "The Moon", "Earth", "Mars", "Venus", "medium"),
("This scale measures earthquake strength.", "The Richter scale", "The Beaufort scale", "The Fujita scale", "The pH scale", "medium"),
("This scale measures wind at sea.", "The Beaufort scale", "The Richter scale", "The Mohs scale", "The Fujita scale", "hard"),
("This scale measures mineral hardness.", "The Mohs scale", "The Richter scale", "The pH scale", "The Kelvin scale", "hard"),
("Pure water has a pH of about this.", "7", "0", "14", "1", "medium"),
("This pH is strongly acidic.", "1", "7", "14", "10", "medium"),
("Lightning is a discharge of this.", "Electricity", "Magnetism", "Sound", "Heat only", "easy"),
]
for q, a, b, c, d, diff in science2:
    put("Science", diff, q, a, b, c, d)

# grammar fix: "This gas do plants" is bad. Fix by not including it - I'll overwrite that question if present.
for i, row in enumerate(ROWS):
    if row[2].startswith("This gas do plants"):
        ROWS[i] = ("Science", "easy", "Plants release this gas during photosynthesis.", "Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen")

foods2 = [
("This breakfast food is a round flat cake cooked on a griddle.", "A pancake", "A waffle", "A crepe", "French toast", "easy"),
("This breakfast food is cooked in a waffle iron.", "A waffle", "A pancake", "A biscuit", "A scone", "easy"),
("This yellow fruit is peeled before eating the inside.", "A banana", "A lemon", "A mango", "An apple", "easy"),
("This red fruit is often paired with peanut butter.", "An apple", "A strawberry", "A tomato", "A cherry", "easy"),
("This fruit is dried to make raisins.", "Grapes", "Plums", "Cherries", "Figs", "easy"),
("This fruit is dried to make prunes.", "Plums", "Grapes", "Apricots", "Dates", "medium"),
("Ketchup is made mainly from this.", "Tomatoes", "Peppers", "Beets", "Apples", "easy"),
("Peanut butter is ground from these.", "Peanuts", "Almonds", "Cashews", "Sunflower seeds", "easy"),
("This spice colors curry yellow.", "Turmeric", "Paprika", "Cumin", "Saffron", "medium"),
("This expensive spice comes from crocus flowers.", "Saffron", "Vanilla", "Cardamom", "Turmeric", "hard"),
("This sweetener comes from bees.", "Honey", "Maple syrup", "Molasses", "Agave", "easy"),
("This white crystal seasons almost every savory dish.", "Salt", "Sugar", "Baking soda", "Flour", "easy"),
("This grain is ground to make flour for bread.", "Wheat", "Rice", "Corn", "Oats", "easy"),
("This Mexican flatbread wraps a burrito.", "A tortilla", "A pita", "Naan", "A crepe", "easy"),
("This Italian rice dish is stirred until creamy.", "Risotto", "Paella", "Pilaf", "Polenta", "medium"),
("This Spanish rice dish often includes saffron.", "Paella", "Risotto", "Jambalaya", "Biryani", "medium"),
("This Louisiana rice dish mixes meat and vegetables.", "Jambalaya", "Gumbo", "Etouffee", "Paella", "medium"),
("This New Orleans stew often starts with a roux.", "Gumbo", "Jambalaya", "Chowder", "Bisque", "medium"),
("This cold Spanish tomato soup is blended and raw.", "Gazpacho", "Bisque", "Minestrone", "Vichyssoise", "hard"),
("This Japanese broth noodle bowl is called this.", "Ramen", "Udon", "Soba", "Pho", "easy"),
]
for q, a, b, c, d, diff in foods2:
    put("Food & Drink", diff, q, a, b, c, d)

board = [
("This game uses a board of 64 squares and two armies.", "Chess", "Checkers", "Go", "Backgammon", "easy"),
("In this game you try to say checkmate.", "Chess", "Checkers", "Go", "Risk", "easy"),
("This game uses letter tiles to make words.", "Scrabble", "Bananagrams", "Boggle", "Scattergories", "easy"),
("This guessing game uses a hidden picture.", "Pictionary", "Charades", "Cranium", "Taboo", "easy"),
("This party game acts out phrases without speaking.", "Charades", "Pictionary", "Telephone", "Mafia", "easy"),
("This card game asks you to draw 2 or draw 4.", "Uno", "Crazy Eights", "Skip-Bo", "Phase 10", "easy"),
("This property game uses a board, houses, and hotels.", "Monopoly", "The Game of Life", "Clue", "Risk", "easy"),
("This mystery game takes place in a mansion.", "Clue", "Mafia", "Mystery Date", "Scotland Yard", "easy"),
("This war game uses armies on a world map.", "Risk", "Axis and Allies", "Stratego", "Diplomacy", "medium"),
("This ancient Chinese game uses black and white stones.", "Go", "Chess", "Checkers", "Reversi", "medium"),
]
for q, a, b, c, d, diff in board:
    put("General Knowledge", diff, q, a, b, c, d)

jobs = [
("This person flies a commercial airplane.", "A pilot", "A captain of a ship", "A conductor", "A driver", "easy"),
("This person argues cases in court.", "A lawyer", "A judge", "A juror", "A clerk", "easy"),
("This person leads an orchestra.", "A conductor", "A composer", "A drummer", "A producer", "medium"),
("This person designs buildings.", "An architect", "An engineer", "A contractor", "A surveyor", "easy"),
("This person writes the news for a paper.", "A journalist", "An editor", "A publisher", "A printer", "easy"),
("This person puts out fires.", "A firefighter", "A police officer", "A paramedic", "A ranger", "easy"),
("This person treats sick animals.", "A veterinarian", "A zoologist", "A doctor", "A trainer", "easy"),
("This person cooks in a restaurant kitchen.", "A chef", "A server", "A host", "A sommelier", "easy"),
]
for q, a, b, c, d, diff in jobs:
    put("General Knowledge", diff, q, a, b, c, d)

weather = [
("Frozen rain that piles up white is called this.", "Snow", "Hail", "Sleet", "Frost", "easy"),
("A spinning storm over warm ocean water is called this in the Atlantic.", "A hurricane", "A typhoon", "A tornado", "A monsoon", "easy"),
("The same kind of storm in the western Pacific is often called this.", "A typhoon", "A tornado", "A monsoon", "A blizzard", "medium"),
("A twisting column of wind over land is called this.", "A tornado", "A hurricane", "A waterspout", "A dust devil", "easy"),
("Water falling from clouds is called this.", "Rain", "Dew", "Fog", "Mist", "easy"),
("A cloud sitting on the ground is called this.", "Fog", "Smog", "Haze", "Steam", "easy"),
("A loud sound after lightning is called this.", "Thunder", "An echo", "A sonic boom", "A landslide", "easy"),
("This is a scientist who studies weather.", "A meteorologist", "A geologist", "An astronomer", "A biologist", "easy"),
]
for q, a, b, c, d, diff in weather:
    put("Science & Nature", diff, q, a, b, c, d)

space = [
("This is the star at the center of our solar system.", "The Sun", "Polaris", "Sirius", "Alpha Centauri", "easy"),
("This galaxy contains our solar system.", "The Milky Way", "Andromeda", "Triangulum", "The Large Magellanic Cloud", "easy"),
("This is the nearest large galaxy to the Milky Way.", "Andromeda", "Triangulum", "Whirlpool", "Sombrero", "hard"),
("This NASA program landed people on the Moon.", "Apollo", "Gemini", "Mercury", "Artemis", "easy"),
("This was the first crewed Moon landing mission.", "Apollo 11", "Apollo 13", "Apollo 8", "Apollo 17", "medium"),
("This Apollo mission is famous for the line Houston, we have a problem.", "Apollo 13", "Apollo 11", "Apollo 1", "Apollo 12", "medium"),
("This rover landed on Mars in 2021 and carries a helicopter.", "Perseverance", "Curiosity", "Opportunity", "Spirit", "hard"),
("This telescope launched in 1990 and orbits Earth.", "Hubble", "James Webb", "Spitzer", "Chandra", "medium"),
("This newer space telescope launched in 2021.", "James Webb", "Hubble", "Kepler", "Gaia", "medium"),
("This dwarf planet was once counted as the ninth planet.", "Pluto", "Ceres", "Eris", "Makemake", "easy"),
]
for q, a, b, c, d, diff in space:
    put("Science", diff, q, a, b, c, d)

lit = [
("This Shakespeare play features the lovers Romeo and Juliet.", "Romeo and Juliet", "Hamlet", "Macbeth", "Othello", "easy"),
("This Shakespeare play features a prince of Denmark.", "Hamlet", "Macbeth", "King Lear", "Othello", "easy"),
("This Shakespeare play features three witches.", "Macbeth", "Hamlet", "The Tempest", "King Lear", "medium"),
("This Shakespeare play features a jealous general named Othello.", "Othello", "Hamlet", "Macbeth", "Julius Caesar", "medium"),
("To be or not to be comes from this play.", "Hamlet", "Macbeth", "Romeo and Juliet", "King Lear", "easy"),
("This novel starts All this happened, more or less, in a war book by Vonnegut.", "Slaughterhouse-Five", "Catch-22", "The Things They Carried", "A Farewell to Arms", "hard"),
("This novel follows Scout and Atticus in Maycomb.", "To Kill a Mockingbird", "The Help", "Go Set a Watchman", "Of Mice and Men", "easy"),
("This novel follows Jay Gatsby and a green light.", "The Great Gatsby", "Tender Is the Night", "This Side of Paradise", "The Sun Also Rises", "medium"),
("This novel follows a boy named Holden Caulfield.", "The Catcher in the Rye", "A Separate Peace", "The Outsiders", "Lord of the Flies", "medium"),
("This novel follows children stranded without adults.", "Lord of the Flies", "The Lord of the Rings", "The Beach", "Swiss Family Robinson", "medium"),
]
for q, a, b, c, d, diff in lit:
    put("Entertainment: Books", diff, q, a, b, c, d)

music_facts = [
("This family of instruments includes trumpet, trombone, and tuba.", "Brass", "Woodwind", "Strings", "Percussion", "easy"),
("This family of instruments includes violin, viola, and cello.", "Strings", "Brass", "Woodwind", "Percussion", "easy"),
("This family of instruments includes flute, clarinet, and oboe.", "Woodwind", "Brass", "Strings", "Percussion", "easy"),
("A quartet of singers has this many people.", "4", "3", "5", "8", "easy"),
("A trio has this many performers.", "3", "2", "4", "6", "easy"),
("The beat of a waltz is usually counted in this number.", "3", "4", "2", "6", "medium"),
("Middle C is a note on this instrument's keyboard.", "The piano", "The violin", "The drum", "The flute", "easy"),
("This singer is known as the Queen of Soul.", "Aretha Franklin", "Whitney Houston", "Diana Ross", "Tina Turner", "medium"),
("This band's members included John, Paul, George, and Ringo.", "The Beatles", "The Monkees", "The Who", "The Kinks", "easy"),
("This band's drummer was Neil Peart.", "Rush", "Led Zeppelin", "Queen", "The Who", "hard"),
]
for q, a, b, c, d, diff in music_facts:
    put("Entertainment: Music", diff, q, a, b, c, d)

tv2 = [
("This show's coffee shop is Central Perk.", "Friends", "Seinfeld", "Frasier", "Will and Grace", "easy"),
("This show's boss is Michael Scott.", "The Office", "Parks and Recreation", "Superstore", "30 Rock", "easy"),
("This show's dad is Homer.", "The Simpsons", "Family Guy", "Bob's Burgers", "American Dad", "easy"),
("This show's science teacher becomes Heisenberg.", "Breaking Bad", "Better Call Saul", "Ozark", "Narcos", "easy"),
("This show's kids live in Hawkins.", "Stranger Things", "Dark", "It", "Wednesday", "easy"),
("This show follows the Roy media family.", "Succession", "Billions", "Industry", "Dynasty", "medium"),
("This show is set in a Chicago restaurant kitchen.", "The Bear", "The Menu", "Kitchen Nightmares", "Sweetbitter", "medium"),
("This animated show is set under the sea in a pineapple.", "SpongeBob SquarePants", "Adventure Time", "Bubble Guppies", "Phineas and Ferb", "easy"),
("This show's slayer is Buffy Summers.", "Buffy the Vampire Slayer", "Angel", "Charmed", "Supernatural", "medium"),
("This mockumentary is set at Dunder Mifflin.", "The Office", "Parks and Recreation", "Modern Family", "Abbott Elementary", "easy"),
]
for q, a, b, c, d, diff in tv2:
    put("Entertainment: Television", diff, q, a, b, c, d)

cars = [
("This brand's sports cars include the 911.", "Porsche", "Ferrari", "Lamborghini", "Aston Martin", "medium"),
("This brand makes the Mustang.", "Ford", "Chevrolet", "Dodge", "Pontiac", "easy"),
("This brand makes the Corvette.", "Chevrolet", "Ford", "Dodge", "Cadillac", "easy"),
("This brand's luxury SUVs include the Escalade.", "Cadillac", "Lincoln", "Lexus", "Buick", "medium"),
("This brand makes the Civic.", "Honda", "Toyota", "Nissan", "Mazda", "easy"),
("This brand makes the Camry.", "Toyota", "Honda", "Hyundai", "Kia", "easy"),
("This electric brand is led by cars like the Model 3.", "Tesla", "Rivian", "Lucid", "Polestar", "easy"),
("This brand's prancing horse is on the badge.", "Ferrari", "Lamborghini", "Porsche", "Maserati", "medium"),
]
for q, a, b, c, d, diff in cars:
    put("Vehicles", diff, q, a, b, c, d)

politics = [
("The U.S. Congress has this many chambers.", "2", "1", "3", "4", "easy"),
("The U.S. Senate has this many voting members.", "100", "50", "435", "200", "medium"),
("The U.S. House of Representatives has this many voting members.", "435", "100", "538", "400", "hard"),
("A U.S. presidential term lasts this many years.", "4", "2", "6", "5", "easy"),
("A U.S. senator's term lasts this many years.", "6", "4", "2", "8", "medium"),
("This document begins We the People.", "The Constitution", "The Declaration of Independence", "The Bill of Rights", "The Articles of Confederation", "easy"),
("The first ten amendments are called this.", "The Bill of Rights", "The Federalist Papers", "The Preamble", "The Articles", "medium"),
("This branch of the U.S. government interprets laws.", "The judicial branch", "The executive branch", "The legislative branch", "The military", "medium"),
]
for q, a, b, c, d, diff in politics:
    put("Politics", diff, q, a, b, c, d)
