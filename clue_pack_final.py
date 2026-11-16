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

capitals = [
("France", "Paris"), ("Germany", "Berlin"), ("Italy", "Rome"), ("Spain", "Madrid"),
("Japan", "Tokyo"), ("China", "Beijing"), ("Russia", "Moscow"), ("Canada", "Ottawa"),
("Australia", "Canberra"), ("Mexico", "Mexico City"), ("Brazil", "Brasilia"),
("Egypt", "Cairo"), ("India", "New Delhi"), ("South Korea", "Seoul"),
("Argentina", "Buenos Aires"), ("Greece", "Athens"), ("Turkey", "Ankara"),
("Portugal", "Lisbon"), ("The Netherlands", "Amsterdam"), ("Belgium", "Brussels"),
("Sweden", "Stockholm"), ("Norway", "Oslo"), ("Denmark", "Copenhagen"),
("Finland", "Helsinki"), ("Poland", "Warsaw"), ("Ireland", "Dublin"),
("Switzerland", "Bern"), ("Austria", "Vienna"), ("Thailand", "Bangkok"),
("Vietnam", "Hanoi"), ("Indonesia", "Jakarta"), ("The Philippines", "Manila"),
("Kenya", "Nairobi"), ("Saudi Arabia", "Riyadh"), ("New Zealand", "Wellington"),
("Cuba", "Havana"), ("Chile", "Santiago"), ("Peru", "Lima"),
("Colombia", "Bogota"), ("Iceland", "Reykjavik"), ("Norway2", "Oslo"),
]
# remove Norway2
capitals = [c for c in capitals if c[0] != "Norway2"]
cities = [c for _, c in capitals]
for i, (country, city) in enumerate(capitals):
    diff = "easy" if i < 12 else "medium"
    put("Geography", diff, f"This city is the capital of {country}.", city, *wrongs(cities, city))

states = [
("Alabama", "Montgomery"), ("Alaska", "Juneau"), ("Arizona", "Phoenix"),
("Arkansas", "Little Rock"), ("California", "Sacramento"), ("Colorado", "Denver"),
("Connecticut", "Hartford"), ("Delaware", "Dover"), ("Florida", "Tallahassee"),
("Georgia", "Atlanta"), ("Hawaii", "Honolulu"), ("Idaho", "Boise"),
("Illinois", "Springfield"), ("Indiana", "Indianapolis"), ("Iowa", "Des Moines"),
("Kansas", "Topeka"), ("Kentucky", "Frankfort"), ("Louisiana", "Baton Rouge"),
("Maine", "Augusta"), ("Maryland", "Annapolis"), ("Massachusetts", "Boston"),
("Michigan", "Lansing"), ("Minnesota", "Saint Paul"), ("Mississippi", "Jackson"),
("Missouri", "Jefferson City"), ("Montana", "Helena"), ("Nebraska", "Lincoln"),
("Nevada", "Carson City"), ("New Hampshire", "Concord"), ("New Jersey", "Trenton"),
("New Mexico", "Santa Fe"), ("New York", "Albany"), ("North Carolina", "Raleigh"),
("North Dakota", "Bismarck"), ("Ohio", "Columbus"), ("Oklahoma", "Oklahoma City"),
("Oregon", "Salem"), ("Pennsylvania", "Harrisburg"), ("Rhode Island", "Providence"),
("South Carolina", "Columbia"), ("South Dakota", "Pierre"), ("Tennessee", "Nashville"),
("Texas", "Austin"), ("Utah", "Salt Lake City"), ("Vermont", "Montpelier"),
("Virginia", "Richmond"), ("Washington", "Olympia"), ("West Virginia", "Charleston"),
("Wisconsin", "Madison"), ("Wyoming", "Cheyenne"),
]
sc = [c for _, c in states]
for i, (state, city) in enumerate(states):
    diff = "easy" if state in {"California", "Texas", "New York", "Florida", "Hawaii"} else "medium"
    put("Geography", diff, f"The capital of {state} is this city.", city, *wrongs(sc, city))

oscars = [
("1993", "Schindler's List"), ("1994", "Forrest Gump"), ("1995", "Braveheart"),
("1997", "Titanic"), ("2000", "Gladiator"), ("2001", "A Beautiful Mind"),
("2002", "Chicago"), ("2003", "The Lord of the Rings: The Return of the King"),
("2006", "The Departed"), ("2007", "No Country for Old Men"),
("2008", "Slumdog Millionaire"), ("2009", "The Hurt Locker"),
("2010", "The King's Speech"), ("2011", "The Artist"),
("2012", "Argo"), ("2013", "12 Years a Slave"),
("2014", "Birdman"), ("2015", "Spotlight"),
("2016", "Moonlight"), ("2017", "The Shape of Water"),
("2018", "Green Book"), ("2019", "Parasite"),
("2020", "Nomadland"), ("2021", "CODA"),
("2022", "Everything Everywhere All at Once"), ("2023", "Oppenheimer"),
]
films = [f for _, f in oscars]
for year, film in oscars:
    put("Entertainment: Film", "hard", f"This film won the Oscar for Best Picture for {year}.", film, *wrongs(films, film))

studios = [
("Super Mario Bros.", "Nintendo"), ("The Legend of Zelda", "Nintendo"),
("Pokemon", "Nintendo"), ("Halo", "Xbox Game Studios"),
("Minecraft", "Mojang"), ("Fortnite", "Epic Games"),
("The Last of Us", "Sony"), ("God of War", "Sony"),
("Grand Theft Auto V", "Rockstar Games"), ("Red Dead Redemption 2", "Rockstar Games"),
("Overwatch", "Blizzard"), ("World of Warcraft", "Blizzard"),
("League of Legends", "Riot Games"), ("Valorant", "Riot Games"),
("The Sims", "Maxis"), ("SimCity", "Maxis"),
("Portal", "Valve"), ("Half-Life", "Valve"),
("Candy Crush", "King"), ("Angry Birds", "Rovio"),
]
makers = []
for _, m in studios:
    if m not in makers:
        makers.append(m)
for game, maker in studios:
    put("Entertainment: Video Games", "medium", f"This company makes {game}.", maker, *wrongs(makers, maker))

bones = [
("This bone protects the brain.", "The skull", "The femur", "The pelvis", "The sternum", "easy"),
("This long bone is in the thigh.", "The femur", "The tibia", "The humerus", "The radius", "medium"),
("This bone is in the upper arm.", "The humerus", "The femur", "The ulna", "The fibula", "medium"),
("These bones make up the spine.", "Vertebrae", "Ribs", "Phalanges", "Tarsals", "easy"),
("This bone is often called the collarbone.", "The clavicle", "The scapula", "The sternum", "The humerus", "medium"),
("This bone is the shoulder blade.", "The scapula", "The clavicle", "The pelvis", "The patella", "medium"),
("This bone is the kneecap.", "The patella", "The femur", "The tibia", "The fibula", "easy"),
("This jaw bone holds the lower teeth.", "The mandible", "The maxilla", "The sternum", "The hyoid", "hard"),
]
for q, a, b, c, d, diff in bones:
    put("Science", diff, q, a, b, c, d)

constellations = [
("This constellation is shaped like a hunter with a belt.", "Orion", "Ursa Major", "Cassiopeia", "Draco", "easy"),
("The Big Dipper is part of this constellation.", "Ursa Major", "Ursa Minor", "Orion", "Lyra", "medium"),
("The North Star is in this constellation.", "Ursa Minor", "Ursa Major", "Orion", "Cassiopeia", "medium"),
("This constellation is named for a lion.", "Leo", "Aries", "Taurus", "Virgo", "easy"),
("This constellation is named for a bull.", "Taurus", "Aries", "Leo", "Scorpio", "medium"),
("This constellation is named for a scorpion.", "Scorpius", "Cancer", "Pisces", "Libra", "medium"),
]
for q, a, b, c, d, diff in constellations:
    put("Science", diff, q, a, b, c, d)

units = [
("There are this many inches in a foot.", "12", "10", "6", "36", "easy"),
("There are this many feet in a yard.", "3", "4", "6", "12", "easy"),
("There are this many ounces in a pound.", "16", "12", "8", "10", "medium"),
("There are this many quarts in a gallon.", "4", "2", "8", "6", "medium"),
("There are this many centimeters in a meter.", "100", "10", "1000", "12", "easy"),
("There are this many millimeters in a centimeter.", "10", "100", "1000", "12", "easy"),
("There are this many grams in a kilogram.", "1000", "100", "10", "500", "easy"),
("Water freezes at this many degrees Fahrenheit.", "32", "0", "212", "100", "easy"),
]
for q, a, b, c, d, diff in units:
    put("Science: Mathematics", diff, q, a, b, c, d)

colors = [
("Mixing red and yellow paint makes this color.", "Orange", "Purple", "Green", "Brown", "easy"),
("Mixing blue and red paint makes this color.", "Purple", "Orange", "Green", "Pink", "easy"),
("Mixing blue and yellow paint makes this color.", "Green", "Purple", "Orange", "Teal", "easy"),
("The rainbow color between yellow and blue is this.", "Green", "Orange", "Indigo", "Violet", "easy"),
("A stop sign is this color.", "Red", "Yellow", "Orange", "White", "easy"),
("A yield sign is usually this color.", "Yellow", "Red", "Green", "Blue", "medium"),
("Grass is usually this color.", "Green", "Brown", "Yellow", "Blue", "easy"),
]
for q, a, b, c, d, diff in colors:
    put("General Knowledge", diff, q, a, b, c, d)

chess = [
("This chess piece moves any number of squares in a straight line.", "The rook", "The bishop", "The knight", "The pawn", "medium"),
("This chess piece moves diagonally.", "The bishop", "The rook", "The knight", "The king", "medium"),
("This chess piece moves in an L shape.", "The knight", "The bishop", "The rook", "The queen", "easy"),
("This chess piece is the most powerful and combines rook and bishop moves.", "The queen", "The king", "The rook", "The bishop", "easy"),
("This chess piece must be protected because the game ends if it is trapped.", "The king", "The queen", "The rook", "The knight", "easy"),
("Pawns that reach the far rank can usually become this piece.", "A queen", "A king", "A second pawn", "A board", "medium"),
]
for q, a, b, c, d, diff in chess:
    put("General Knowledge", diff, q, a, b, c, d)

more = [
("Entertainment: Film", "easy", "This film franchise follows a secret agent named Bond.", "James Bond", "Jason Bourne", "Mission: Impossible", "Kingsman"),
("Entertainment: Film", "easy", "This film features a sinking ship and a couple named Jack and Rose.", "Titanic", "Pearl Harbor", "The Poseidon Adventure", "A Night to Remember"),
("Entertainment: Film", "medium", "This 1977 film introduced Luke Skywalker.", "Star Wars", "Star Trek: The Motion Picture", "Close Encounters of the Third Kind", "Superman"),
("Entertainment: Film", "medium", "This director made Jaws, E.T., and Jurassic Park.", "Steven Spielberg", "George Lucas", "James Cameron", "Ridley Scott"),
("Entertainment: Film", "medium", "This director made Inception and The Dark Knight.", "Christopher Nolan", "Denis Villeneuve", "Zack Snyder", "David Fincher"),
("Entertainment: Television", "easy", "Grogu travels with a bounty hunter in this series.", "The Mandalorian", "The Book of Boba Fett", "Andor", "Ahsoka"),
("Entertainment: Television", "medium", "This series follows a time lord called the Doctor.", "Doctor Who", "Quantum Leap", "Timeless", "Travelers"),
("Entertainment: Television", "easy", "This animated series follows a sponge who lives in a pineapple.", "SpongeBob SquarePants", "Patrick Star's show", "Bubble Guppies", "Oswald"),
("Entertainment: Music", "easy", "This Liverpool band included John, Paul, George, and Ringo.", "The Beatles", "The Hollies", "Gerry and the Pacemakers", "The Searchers"),
("Entertainment: Music", "medium", "This composer wrote the opera The Magic Flute.", "Mozart", "Beethoven", "Bach", "Handel"),
("Entertainment: Music", "medium", "This composer wrote Beethoven's Ninth, also called the Choral symphony.", "Beethoven", "Mozart", "Brahms", "Schubert"),
("Entertainment: Music", "hard", "This composer went deaf and still wrote late symphonies.", "Beethoven", "Bach", "Mozart", "Haydn"),
("Sports", "easy", "This trophy is awarded to the NHL champion.", "The Stanley Cup", "The Lombardi Trophy", "The Commissioner's Trophy", "The Claret Jug"),
("Sports", "medium", "This trophy is awarded to the winner of the British Open in golf.", "The Claret Jug", "The Green Jacket", "The Wanamaker Trophy", "The U.S. Open trophy"),
("Sports", "easy", "This sport uses a puck.", "Ice hockey", "Lacrosse", "Field hockey", "Curling"),
("Sports", "easy", "This sport uses a bat and a diamond.", "Baseball", "Cricket", "Softball", "Rounders"),
("Sports", "medium", "Cricket is played with a bat and this object.", "A ball", "A puck", "A shuttlecock", "A disc"),
("Sports", "easy", "This sport is played at Wimbledon on grass.", "Tennis", "Croquet", "Golf", "Bowls"),
("Sports", "medium", "The French Open is played on this surface.", "Clay", "Grass", "Hard court", "Carpet"),
("Sports", "medium", "The U.S. Open tennis tournament is played on this surface.", "Hard court", "Clay", "Grass", "Wood"),
("Food & Drink", "easy", "This fruit is green on the outside and red with black seeds inside.", "Watermelon", "Honeydew", "Cantaloupe", "Papaya"),
("Food & Drink", "easy", "This yellow curved fruit grows in bunches.", "Banana", "Plantain", "Mango", "Papaya"),
("Food & Drink", "easy", "This citrus fruit is sour and yellow.", "Lemon", "Lime", "Orange", "Grapefruit"),
("Food & Drink", "easy", "This citrus fruit is green and sour.", "Lime", "Lemon", "Apple", "Kiwi"),
("Food & Drink", "medium", "This nut is used to make marzipan.", "Almond", "Walnut", "Pecan", "Peanut"),
("Food & Drink", "easy", "Popcorn is made by heating this grain.", "Corn", "Rice", "Wheat", "Barley"),
("Food & Drink", "medium", "This dark sauce is fermented soybeans, wheat, and salt.", "Soy sauce", "Fish sauce", "Oyster sauce", "Hoisin"),
("Animals", "easy", "This farm animal gives milk that is commonly sold in cartons.", "A cow", "A goat", "A sheep", "A horse"),
("Animals", "easy", "This farm animal is raised for wool.", "A sheep", "A goat", "A cow", "A pig"),
("Animals", "easy", "This bird lays the eggs most people buy at the store.", "A chicken", "A duck", "A goose", "A turkey"),
("Animals", "medium", "This sea mammal is known for balancing a ball in shows.", "A dolphin", "A seal", "A walrus", "A sea lion"),
("Animals", "easy", "This animal's baby is called a calf and it has a trunk.", "An elephant", "A rhino", "A hippo", "A giraffe"),
("Animals", "medium", "This reptile is famous for a hard shell and a slow walk.", "A tortoise", "A crocodile", "A lizard", "A snake"),
("History", "easy", "This country gifted the Statue of Liberty to the United States.", "France", "Britain", "Spain", "Italy"),
("History", "medium", "This city was the first capital of the United States under the Constitution.", "New York", "Philadelphia", "Washington", "Boston"),
("History", "hard", "This city hosted the 1936 Summer Olympics.", "Berlin", "London", "Paris", "Rome"),
("History", "medium", "This city hosted the 1996 Summer Olympics.", "Atlanta", "Los Angeles", "Sydney", "Barcelona"),
("History", "medium", "This city hosted the 2012 Summer Olympics.", "London", "Paris", "Beijing", "Athens"),
("History", "easy", "This city hosted the 2024 Summer Olympics.", "Paris", "Los Angeles", "London", "Tokyo"),
("Science", "easy", "This season is the hottest in most of the northern United States.", "Summer", "Spring", "Autumn", "Winter"),
("Science", "easy", "This season brings falling leaves in much of the United States.", "Autumn", "Winter", "Spring", "Summer"),
("Science", "medium", "This scientist developed the laws of motion and universal gravitation.", "Isaac Newton", "Albert Einstein", "Galileo Galilei", "Johannes Kepler"),
("Science", "medium", "This scientist improved the telescope and supported a sun-centered solar system.", "Galileo Galilei", "Isaac Newton", "Nicolaus Copernicus", "Tycho Brahe"),
("Science", "hard", "This scientist proposed that planets orbit the Sun in ellipses.", "Johannes Kepler", "Nicolaus Copernicus", "Galileo Galilei", "Isaac Newton"),
("Mythology", "easy", "This hero stole fire for humans in a famous Greek tale.", "Prometheus", "Heracles", "Odysseus", "Icarus"),
("Mythology", "medium", "This boy flew too close to the sun on wax wings.", "Icarus", "Daedalus", "Perseus", "Bellerophon"),
("Mythology", "medium", "This hero slew the Minotaur in a labyrinth.", "Theseus", "Perseus", "Heracles", "Jason"),
("Mythology", "medium", "This hero sought the Golden Fleece.", "Jason", "Theseus", "Perseus", "Odysseus"),
("Art", "easy", "The painting of a woman with a mysterious smile is this.", "The Mona Lisa", "The Starry Night", "Girl with a Pearl Earring", "American Gothic"),
("Art", "medium", "A swirling night sky over a village is this painting.", "The Starry Night", "The Scream", "Water Lilies", "Guernica"),
("Entertainment: Books", "easy", "This author created Winnie-the-Pooh.", "A.A. Milne", "Beatrix Potter", "Roald Dahl", "Dr. Seuss"),
("Entertainment: Books", "easy", "This author wrote The Cat in the Hat.", "Dr. Seuss", "Eric Carle", "Mo Willems", "Shel Silverstein"),
("Entertainment: Books", "medium", "This author wrote The Outsiders.", "S.E. Hinton", "J.D. Salinger", "Judy Blume", "Lois Lowry"),
("Entertainment: Books", "medium", "This author wrote The Giver.", "Lois Lowry", "Suzanne Collins", "Veronica Roth", "Madeleine L'Engle"),
("Entertainment: Video Games", "easy", "This game asks you to catch 'em all.", "Pokemon", "Digimon", "Yo-kai Watch", "Temtem"),
("Entertainment: Video Games", "medium", "This game stars a spartan in green armor.", "Halo", "Doom", "Gears of War", "Titanfall"),
("Entertainment: Video Games", "easy", "Blocks, creepers, and crafting define this game.", "Minecraft", "Roblox", "Terraria", "Fortnite"),
("Celebrities", "easy", "This singer is known as the Queen of Pop.", "Madonna", "Beyonce", "Lady Gaga", "Britney Spears"),
("Celebrities", "medium", "This actor played Jack in Titanic.", "Leonardo DiCaprio", "Brad Pitt", "Matt Damon", "Johnny Depp"),
("Celebrities", "medium", "This actor played Rose in Titanic.", "Kate Winslet", "Nicole Kidman", "Cate Blanchett", "Rachel McAdams"),
("General Knowledge", "easy", "This many cents are in a U.S. dollar.", "100", "10", "50", "20"),
("General Knowledge", "easy", "This coin is worth 25 cents.", "A quarter", "A dime", "A nickel", "A penny"),
("General Knowledge", "easy", "This coin is worth 10 cents.", "A dime", "A nickel", "A quarter", "A half-dollar"),
("General Knowledge", "easy", "This coin is worth 5 cents.", "A nickel", "A dime", "A penny", "A quarter"),
("General Knowledge", "easy", "This coin is worth 1 cent.", "A penny", "A nickel", "A dime", "A quarter"),
("General Knowledge", "medium", "A standard deck of playing cards has this many cards.", "52", "48", "54", "50"),
("General Knowledge", "medium", "There are this many suits in a standard deck.", "4", "3", "5", "2"),
("Politics", "easy", "The president of the United States lives in this house.", "The White House", "The Capitol", "The Pentagon", "Mount Vernon"),
("Politics", "medium", "Laws in the United States are signed by this official.", "The president", "The chief justice", "The speaker of the House", "The vice president"),
("Vehicles", "easy", "This vehicle travels on rails between cities.", "A train", "A bus", "A ferry", "A bicycle"),
("Vehicles", "easy", "This vehicle flies using wings and engines.", "An airplane", "A helicopter", "A blimp", "A glider"),
("Vehicles", "medium", "This aircraft has a spinning rotor on top.", "A helicopter", "An airplane", "A jet", "A glider"),
("Science & Nature", "easy", "This layer of gas surrounds Earth.", "The atmosphere", "The crust", "The mantle", "The ocean"),
("Science & Nature", "medium", "This layer of Earth is the solid ground we stand on.", "The crust", "The mantle", "The core", "The atmosphere"),
("Science & Nature", "easy", "This star is closest to Earth.", "The Sun", "Proxima Centauri", "Sirius", "Polaris"),
]
for cat, diff, q, a, b, c, d in more:
    put(cat, diff, q, a, b, c, d)
