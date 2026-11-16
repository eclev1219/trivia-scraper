ROWS = []

def put(cat, diff, q, a, b, c, d):
    ROWS.append((cat, diff, q, a, b, c, d))

def wrongs(pool, answer, n=3):
    out = []
    for item in pool:
        if item != answer and item not in out:
            out.append(item)
        if len(out) == n:
            break
    return out

elements = [
("H", "Hydrogen"), ("He", "Helium"), ("Li", "Lithium"), ("C", "Carbon"),
("N", "Nitrogen"), ("O", "Oxygen"), ("F", "Fluorine"), ("Ne", "Neon"),
("Na", "Sodium"), ("Mg", "Magnesium"), ("Al", "Aluminum"), ("Si", "Silicon"),
("P", "Phosphorus"), ("S", "Sulfur"), ("Cl", "Chlorine"), ("K", "Potassium"),
("Ca", "Calcium"), ("Fe", "Iron"), ("Cu", "Copper"), ("Zn", "Zinc"),
("Ag", "Silver"), ("Au", "Gold"), ("Hg", "Mercury"), ("Pb", "Lead"),
("U", "Uranium"), ("Sn", "Tin"), ("Ni", "Nickel"), ("Co", "Cobalt"),
]
names = [n for _, n in elements]
for i, (sym, name) in enumerate(elements):
    w = wrongs(names[i:] + names, name)
    diff = "easy" if sym in {"H", "O", "C", "Au", "Fe"} else "medium"
    put("Science", diff, f"The chemical symbol {sym} stands for this element.", name, *w)

planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
order_facts = [
(1, "Mercury"), (2, "Venus"), (3, "Earth"), (4, "Mars"),
(5, "Jupiter"), (6, "Saturn"), (7, "Uranus"), (8, "Neptune"),
]
for n, name in order_facts:
    w = wrongs(planets, name)
    put("Science", "medium", f"This planet is number {n} from the Sun.", name, *w)

moons = {"Earth": "1", "Mars": "2", "Jupiter": "95", "Saturn": "146"}
# Jupiter and Saturn moon counts change. Skip exact counts except Earth and Mars.
put("Science", "easy", "Earth has this many moons.", "1", "0", "2", "4")
put("Science", "medium", "Mars has this many moons.", "2", "1", "0", "4")

inventions = [
("the telephone", "Alexander Graham Bell", ("Thomas Edison", "Nikola Tesla", "Guglielmo Marconi")),
("the practical light bulb", "Thomas Edison", ("Nikola Tesla", "Alexander Graham Bell", "Benjamin Franklin")),
("the first successful airplane flight", "The Wright brothers", ("The Montgolfier brothers", "Charles Lindbergh", "Amelia Earhart")),
("the theory of relativity people quote", "Albert Einstein", ("Isaac Newton", "Galileo Galilei", "Stephen Hawking")),
("penicillin", "Alexander Fleming", ("Louis Pasteur", "Jonas Salk", "Edward Jenner")),
("the polio vaccine", "Jonas Salk", ("Albert Sabin", "Alexander Fleming", "Louis Pasteur")),
("the World Wide Web", "Tim Berners-Lee", ("Bill Gates", "Steve Jobs", "Vint Cerf")),
]
for what, who, w in inventions:
    put("History", "medium", f"This person is credited with {what}.", who, *w)

disney = [
("Elsa", "Frozen"), ("Moana", "Moana"), ("Simba", "The Lion King"),
("Ariel", "The Little Mermaid"), ("Belle", "Beauty and the Beast"),
("Aladdin", "Aladdin"), ("Mulan", "Mulan"), ("Pocahontas", "Pocahontas"),
("Tiana", "The Princess and the Frog"), ("Rapunzel", "Tangled"),
("Merida", "Brave"), ("Anna", "Frozen"), ("Maui", "Moana"),
("Olaf", "Frozen"), ("Genie", "Aladdin"), ("Mufasa", "The Lion King"),
("Scar", "The Lion King"), ("Ursula", "The Little Mermaid"),
("Jafar", "Aladdin"), ("Maleficent", "Sleeping Beauty"),
("Cinderella", "Cinderella"), ("Snow White", "Snow White and the Seven Dwarfs"),
("Aurora", "Sleeping Beauty"), ("Stitch", "Lilo and Stitch"),
("Baymax", "Big Hero 6"), ("Ralph", "Wreck-It Ralph"),
]
films = []
for _, film in disney:
    if film not in films:
        films.append(film)
for i, (who, film) in enumerate(disney):
    diff = "easy" if i < 12 else "medium"
    put("Entertainment: Film", diff, f"{who} is a character in this Disney film.", film, *wrongs(films, film))

pixar = [
("Woody", "Toy Story"), ("Buzz Lightyear", "Toy Story"), ("Nemo", "Finding Nemo"),
("Dory", "Finding Nemo"), ("Mike Wazowski", "Monsters, Inc."), ("Sulley", "Monsters, Inc."),
("Mr. Incredible", "The Incredibles"), ("Elastigirl", "The Incredibles"),
("Remy", "Ratatouille"), ("Linguini", "Ratatouille"),
("Wall-E", "WALL-E"), ("Eve", "WALL-E"), ("Carl", "Up"), ("Russell", "Up"),
("Joy", "Inside Out"), ("Sadness", "Inside Out"), ("Miguel", "Coco"),
("Lightning McQueen", "Cars"), ("Mater", "Cars"),
]
pf = []
for _, film in pixar:
    if film not in pf:
        pf.append(film)
for who, film in pixar:
    put("Entertainment: Film", "easy", f"{who} is a main character in this Pixar film.", film, *wrongs(pf, film))

marvel = [
("Tony Stark", "Iron Man"), ("Steve Rogers", "Captain America"),
("Thor", "Thor"), ("Bruce Banner", "Hulk"), ("Natasha Romanoff", "Black Widow"),
("Clint Barton", "Hawkeye"), ("Peter Parker", "Spider-Man"),
("T'Challa", "Black Panther"), ("Stephen Strange", "Doctor Strange"),
("Scott Lang", "Ant-Man"), ("Carol Danvers", "Captain Marvel"),
("Wanda Maximoff", "Scarlet Witch"), ("Vision", "Vision"),
("Loki", "Loki"), ("Nick Fury", "Nick Fury"),
("Peter Quill", "Star-Lord"), ("Gamora", "Gamora"),
("Drax", "Drax"), ("Rocket", "Rocket Raccoon"), ("Groot", "Groot"),
]
for name, hero in marvel:
    put("Entertainment: Film", "medium", f"In the Marvel films, {name} is this hero.", hero, *wrongs([h for _, h in marvel], hero))

actors = [
("Robert Downey Jr.", "Iron Man"), ("Chris Evans", "Captain America"),
("Chris Hemsworth", "Thor"), ("Mark Ruffalo", "Hulk"),
("Scarlett Johansson", "Black Widow"), ("Tom Holland", "Spider-Man"),
("Chadwick Boseman", "Black Panther"), ("Benedict Cumberbatch", "Doctor Strange"),
("Paul Rudd", "Ant-Man"), ("Brie Larson", "Captain Marvel"),
("Chris Pratt", "Star-Lord"), ("Zoe Saldana", "Gamora"),
("Tom Hiddleston", "Loki"), ("Elizabeth Olsen", "Scarlet Witch"),
("Jeremy Renner", "Hawkeye"), ("Samuel L. Jackson", "Nick Fury"),
]
for actor, hero in actors:
    put("Celebrities", "medium", f"This actor plays {hero} in the Marvel films.", actor, *wrongs([a for a, _ in actors], actor))

starwars = [
("Luke Skywalker", "A farm boy who trains as a Jedi"),
("Leia Organa", "A princess and rebel leader"),
("Han Solo", "A smuggler who pilots the Millennium Falcon"),
("Darth Vader", "A Sith lord in black armor"),
("Yoda", "A small green Jedi master"),
("Obi-Wan Kenobi", "A Jedi who watches over Luke"),
("Chewbacca", "A Wookiee co-pilot"),
("R2-D2", "A brave astromech droid"),
("C-3PO", "A protocol droid who worries a lot"),
("Palpatine", "The emperor of the Galactic Empire"),
]
for name, role in starwars:
    put("Entertainment: Film", "easy", f"In Star Wars, {role[0].lower() + role[1:]} is this character.", name, *wrongs([n for n, _ in starwars], name))

hp = [
("Harry Potter", "The boy who lived"),
("Hermione Granger", "The brightest witch of her age"),
("Ron Weasley", "Harry's red-haired best friend"),
("Albus Dumbledore", "Hogwarts headmaster"),
("Severus Snape", "Potions master with a complicated past"),
("Lord Voldemort", "The dark wizard who must not be named"),
("Rubeus Hagrid", "Keeper of keys and grounds"),
("Draco Malfoy", "A rival from Slytherin"),
("Minerva McGonagall", "Head of Gryffindor"),
("Sirius Black", "Harry's godfather"),
]
for name, role in hp:
    put("Entertainment: Film", "easy", f"In the Harry Potter films, {role[0].lower() + role[1:]} is this character.", name, *wrongs([n for n, _ in hp], name))

songs2 = [
("Queen", "We Will Rock You"), ("Queen", "We Are the Champions"),
("Queen", "Another One Bites the Dust"), ("The Beatles", "Let It Be"),
("The Beatles", "Yesterday"), ("The Beatles", "Help!"),
("The Rolling Stones", "Satisfaction"), ("The Rolling Stones", "Paint It Black"),
("Michael Jackson", "Beat It"), ("Michael Jackson", "Billie Jean"),
("Madonna", "Material Girl"), ("Madonna", "Like a Prayer"),
("Taylor Swift", "Blank Space"), ("Taylor Swift", "Love Story"),
("Beyonce", "Halo"), ("Beyonce", "Irreplaceable"),
("Drake", "God's Plan"), ("Drake", "Hotline Bling"),
("Eminem", "Stan"), ("Eminem", "The Real Slim Shady"),
("Adele", "Someone Like You"), ("Adele", "Set Fire to the Rain"),
("Elvis Presley", "Jailhouse Rock"), ("Elvis Presley", "Hound Dog"),
("Johnny Cash", "Folsom Prison Blues"), ("Johnny Cash", "Ring of Fire"),
("Bob Dylan", "Blowin' in the Wind"), ("Bob Dylan", "Like a Rolling Stone"),
("Aretha Franklin", "Respect"), ("Stevie Wonder", "Superstition"),
("Prince", "When Doves Cry"), ("Prince", "Kiss"),
("David Bowie", "Space Oddity"), ("David Bowie", "Heroes"),
("Elton John", "Your Song"), ("Elton John", "Rocket Man"),
("ABBA", "Mamma Mia"), ("ABBA", "Dancing Queen"),
("Nirvana", "Come As You Are"), ("Nirvana", "Heart-Shaped Box"),
("AC/DC", "Highway to Hell"), ("AC/DC", "Back in Black"),
("Led Zeppelin", "Kashmir"), ("Led Zeppelin", "Black Dog"),
("Pink Floyd", "Another Brick in the Wall"), ("Pink Floyd", "Wish You Were Here"),
("Fleetwood Mac", "Dreams"), ("Fleetwood Mac", "The Chain"),
("Eagles", "Take It Easy"), ("Eagles", "Desperado"),
("Bruce Springsteen", "Born in the U.S.A."), ("Bruce Springsteen", "Dancing in the Dark"),
("Whitney Houston", "I Wanna Dance with Somebody"), ("Mariah Carey", "All I Want for Christmas Is You"),
("Celine Dion", "My Heart Will Go On"), ("Bruno Mars", "24K Magic"),
("The Weeknd", "Save Your Tears"), ("Billie Eilish", "Happier Than Ever"),
("Harry Styles", "Watermelon Sugar"), ("Dua Lipa", "Don't Start Now"),
("Lady Gaga", "Shallow"), ("Rihanna", "Diamonds"),
("Katy Perry", "Roar"), ("Justin Bieber", "Sorry"),
("Ed Sheeran", "Perfect"), ("Olivia Rodrigo", "vampire"),
("Kendrick Lamar", "HUMBLE."), ("Travis Scott", "Sicko Mode"),
("Outkast", "Ms. Jackson"), ("Jay-Z", "99 Problems"),
("Alicia Keys", "Fallin'"), ("John Legend", "All of Me"),
("Sam Smith", "Stay With Me"), ("Lewis Capaldi", "Someone You Loved"),
("Miley Cyrus", "Party in the U.S.A."), ("Dolly Parton", "Jolene"),
("Shania Twain", "Man! I Feel Like a Woman!"), ("Garth Brooks", "Friends in Low Places"),
("Ray Charles", "Georgia on My Mind"), ("Otis Redding", "Sittin' on the Dock of the Bay"),
("Marvin Gaye", "Let's Get It On"), ("James Brown", "I Got You (I Feel Good)"),
("Chuck Berry", "Johnny B. Goode"), ("Little Richard", "Tutti Frutti"),
("The Beach Boys", "Good Vibrations"), ("Simon and Garfunkel", "The Sound of Silence"),
("Simon and Garfunkel", "Bridge Over Troubled Water"), ("The Who", "Pinball Wizard"),
("Jimi Hendrix", "All Along the Watchtower"), ("Eric Clapton", "Tears in Heaven"),
("U2", "One"), ("Coldplay", "Fix You"),
("Radiohead", "Karma Police"), ("Oasis", "Don't Look Back in Anger"),
("Red Hot Chili Peppers", "Californication"), ("Green Day", "Basket Case"),
("Blink-182", "All the Small Things"), ("Linkin Park", "In the End"),
("Metallica", "Nothing Else Matters"), ("Black Sabbath", "Iron Man"),
("Guns N' Roses", "November Rain"), ("Bon Jovi", "It's My Life"),
("Journey", "Separate Ways"), ("Toto", "Africa"),
("a-ha", "Take On Me"), ("Europe", "The Final Countdown"),
("Queen", "Don't Stop Me Now"), ("The Beatles", "Here Comes the Sun"),
]
artists = []
seen_a = []
for a, _s in songs2:
    if a not in seen_a:
        seen_a.append(a)
artists = seen_a
for i, (artist, song) in enumerate(songs2):
    w = wrongs(artists, artist)
    diff = "easy" if i % 3 == 0 else "medium"
    put("Entertainment: Music", diff, f"This act recorded {song}.", artist, *w)

sports_nums = [
("A safety in American football is worth this many points.", "2", "1", "3", "6", "easy"),
("A successful extra point is worth this many points.", "1", "2", "3", "6", "easy"),
("A free throw in basketball is worth this many points.", "1", "2", "3", "4", "easy"),
("A shot from beyond the arc in basketball is worth this many points.", "3", "2", "1", "4", "easy"),
("A soccer goal is worth this many points.", "1", "2", "3", "6", "easy"),
("An ice hockey goal is worth this many points.", "1", "2", "3", "5", "easy"),
("One lap around the bases on a home run scores this.", "A run", "A point", "A goal", "A down", "easy"),
("Three goals by one player in a game is called this.", "A hat trick", "A triple double", "A grand slam", "A turkey", "medium"),
("Four bases on one hit is called this.", "A home run", "A triple", "A double", "A single", "easy"),
("A score of zero in tennis is called this.", "Love", "Nil", "Deuce", "Advantage", "easy"),
("When both tennis players reach 40, the score is called this.", "Deuce", "Love", "Advantage", "Set", "medium"),
("A hole in one in golf is also called this.", "An ace", "An eagle", "A birdie", "A bogey", "medium"),
("One over par on a golf hole is called this.", "A bogey", "A birdie", "A par", "A double eagle", "easy"),
("The Olympic symbol has this many rings.", "5", "4", "6", "7", "easy"),
("Summer Olympics are normally held this many years apart.", "4", "2", "3", "5", "easy"),
("An NFL quarter lasts this many minutes.", "15", "12", "10", "20", "medium"),
("An NBA quarter lasts this many minutes.", "12", "15", "10", "8", "medium"),
("A soccer half lasts this many minutes.", "45", "40", "30", "60", "medium"),
("A regulation hockey period lasts this many minutes.", "20", "15", "10", "12", "medium"),
("There are this many pins in ten-pin bowling.", "10", "9", "12", "8", "easy"),
("A strike in baseball is part of a count that ends at this many strikes.", "3", "4", "2", "5", "easy"),
("A walk in baseball happens after this many balls.", "4", "3", "5", "6", "medium"),
("The Kentucky Derby is a race for these animals.", "Horses", "Dogs", "Cars", "Boats", "easy"),
("The Indianapolis 500 is a race for these.", "Cars", "Horses", "Boats", "Motorcycles", "easy"),
("The Champions League is a club tournament in this sport.", "Soccer", "Basketball", "Ice hockey", "Rugby", "easy"),
("The Ashes is a rivalry in this sport.", "Cricket", "Rugby", "Tennis", "Golf", "hard"),
("The Heisman Trophy honors the top player in this college sport.", "Football", "Basketball", "Baseball", "Hockey", "medium"),
("The Cy Young Award honors the best pitcher in this sport.", "Baseball", "Softball", "Cricket", "Football", "medium"),
("Number 12 was worn by this Patriots quarterback.", "Tom Brady", "Drew Bledsoe", "Mac Jones", "Cam Newton", "easy"),
("Number 15 is worn by this Chiefs quarterback.", "Patrick Mahomes", "Josh Allen", "Joe Burrow", "Lamar Jackson", "medium"),
("Number 30 is worn by this Warriors shooter.", "Stephen Curry", "Klay Thompson", "Draymond Green", "Kevin Durant", "easy"),
("This Lakers legend wore both 8 and 24.", "Kobe Bryant", "Magic Johnson", "Shaquille O'Neal", "Kareem Abdul-Jabbar", "easy"),
("This Bulls forward was Jordan's longtime teammate and wore 33.", "Scottie Pippen", "Dennis Rodman", "Horace Grant", "Toni Kukoc", "medium"),
("This Celtics legend wore 33.", "Larry Bird", "Bill Russell", "Bob Cousy", "Paul Pierce", "medium"),
("This Lakers center wore number 34.", "Shaquille O'Neal", "Kareem Abdul-Jabbar", "Wilt Chamberlain", "Pau Gasol", "medium"),
]
for q, a, b, c, d, diff in sports_nums:
    put("Sports", diff, q, a, b, c, d)

world_cups = [
("1930", "Uruguay"), ("1934", "Italy"), ("1938", "Italy"), ("1950", "Uruguay"),
("1954", "West Germany"), ("1958", "Brazil"), ("1962", "Brazil"), ("1966", "England"),
("1970", "Brazil"), ("1974", "West Germany"), ("1978", "Argentina"), ("1982", "Italy"),
("1986", "Argentina"), ("1990", "Germany"), ("1994", "Brazil"), ("1998", "France"),
("2002", "Brazil"), ("2006", "Italy"), ("2010", "Spain"), ("2014", "Germany"),
("2018", "France"), ("2022", "Argentina"),
]
winners = []
for _, w in world_cups:
    if w not in winners:
        winners.append(w)
for year, winner in world_cups:
    w = wrongs(winners, winner)
    diff = "easy" if year in {"2018", "2022", "2014", "2010"} else "medium"
    put("Sports", diff, f"This country won the men's FIFA World Cup in {year}.", winner, *w)

bodies = [
("The femur is a bone in this part of the body.", "The leg", "The arm", "The skull", "The spine", "medium"),
("The skull protects this organ.", "The brain", "The heart", "The lungs", "The liver", "easy"),
("The ribs mainly protect these organs.", "The heart and lungs", "The stomach and liver", "The kidneys", "The brain", "easy"),
("People see with these organs.", "The eyes", "The ears", "The nose", "The skin", "easy"),
("People hear with these organs.", "The ears", "The eyes", "The nose", "The tongue", "easy"),
("This organ makes insulin.", "The pancreas", "The liver", "The kidney", "The spleen", "medium"),
("This organ produces bile.", "The liver", "The stomach", "The pancreas", "The gallbladder", "hard"),
("This organ stores bile.", "The gallbladder", "The liver", "The pancreas", "The appendix", "hard"),
("Adults normally have this many teeth, including wisdom teeth.", "32", "28", "30", "24", "medium"),
("A human hand has this many fingers, counting the thumb.", "5", "4", "6", "10", "easy"),
("This blood cells carry oxygen.", "Red blood cells", "White blood cells", "Platelets", "Plasma", "medium"),
("These blood cells help fight infection.", "White blood cells", "Red blood cells", "Platelets", "Plasma", "medium"),
("This part of the blood helps clotting.", "Platelets", "Red blood cells", "Plasma", "White blood cells", "hard"),
]
for q, a, b, c, d, diff in bodies:
    put("Science", diff, q, a, b, c, d)

mathq = [
("A square has this many sides.", "4", "3", "5", "6", "easy"),
("A pentagon has this many sides.", "5", "6", "4", "8", "easy"),
("An octagon has this many sides.", "8", "6", "10", "7", "easy"),
("A right angle measures this many degrees.", "90", "45", "180", "360", "easy"),
("A straight angle measures this many degrees.", "180", "90", "360", "270", "medium"),
("A full circle measures this many degrees.", "360", "180", "90", "270", "easy"),
("The value of pi is a little more than this whole number.", "3", "4", "2", "5", "easy"),
("Ten times ten equals this.", "100", "20", "1000", "50", "easy"),
("A prime number has exactly this many positive divisors.", "2", "1", "3", "4", "hard"),
("The first prime number is this.", "2", "1", "3", "0", "medium"),
("There are this many degrees in a triangle's interior angles added together.", "180", "90", "360", "270", "medium"),
]
for q, a, b, c, d, diff in mathq:
    put("Science: Mathematics", diff, q, a, b, c, d)

gk = [
("There are this many months in a year.", "12", "10", "11", "13", "easy"),
("There are this many hours in a day.", "24", "12", "48", "36", "easy"),
("There are this many minutes in an hour.", "60", "100", "30", "24", "easy"),
("There are this many seconds in a minute.", "60", "100", "30", "10", "easy"),
("There are this many days in a week.", "7", "5", "6", "8", "easy"),
("February has this many days in a leap year.", "29", "28", "30", "31", "easy"),
("This month has 28 days in a common year.", "February", "April", "June", "November", "easy"),
("Christmas Day is in this month.", "December", "November", "January", "October", "easy"),
("Halloween falls in this month.", "October", "September", "November", "December", "easy"),
("New Year's Day is the first day of this month.", "January", "December", "March", "June", "easy"),
("This holiday uses hearts and falls in February.", "Valentine's Day", "Halloween", "Thanksgiving", "Easter", "easy"),
("A score, as in four score, means this many.", "20", "10", "40", "12", "hard"),
("A baker's dozen is this many.", "13", "12", "11", "14", "medium"),
("A gross is this many.", "144", "100", "120", "12", "hard"),
("The Pacific Ocean is larger than this ocean.", "The Atlantic", "The Pacific itself", "Both polar seas together", "The sky", "easy"),
]
for q, a, b, c, d, diff in gk:
    put("General Knowledge", diff, q, a, b, c, d)

instruments = [
("This instrument has 88 keys.", "The piano", "The organ", "The harpsichord", "The accordion", "easy"),
("This instrument is played with a bow and has four strings.", "The violin", "The guitar", "The harp", "The banjo", "easy"),
("This large string instrument is played upright or with an endpin.", "The cello", "The viola", "The double bass", "The violin", "medium"),
("This brass instrument has a slide.", "The trombone", "The trumpet", "The French horn", "The tuba", "easy"),
("This woodwind uses a single reed and is common in jazz.", "The saxophone", "The flute", "The oboe", "The bassoon", "medium"),
("This instrument is a hollow box with six strings, often strummed.", "The guitar", "The violin", "The harp", "The ukulele", "easy"),
("This small four-string instrument is popular in Hawaii.", "The ukulele", "The banjo", "The mandolin", "The lute", "easy"),
("Drummers strike these with sticks.", "Drums", "Cymbals only", "Bongos only", "Timpani only", "easy"),
]
for q, a, b, c, d, diff in instruments:
    put("Entertainment: Music", diff, q, a, b, c, d)

fairy = [
("This girl loses a glass slipper.", "Cinderella", "Snow White", "Sleeping Beauty", "Rapunzel", "easy"),
("This girl eats a poisoned apple.", "Snow White", "Cinderella", "Belle", "Ariel", "easy"),
("This girl sleeps after a spindle prick.", "Sleeping Beauty", "Snow White", "Cinderella", "Rapunzel", "easy"),
("This girl lets down very long hair.", "Rapunzel", "Cinderella", "Merida", "Elsa", "easy"),
("This boy trades a cow for beans.", "Jack", "Hansel", "Aladdin", "Pinocchio", "easy"),
("These two children find a candy house.", "Hansel and Gretel", "Jack and Jill", "Romulus and Remus", "Mary and Joseph", "easy"),
("This puppet wants to be a real boy.", "Pinocchio", "Peter Pan", "Woody", "Geppetto", "easy"),
("This wolf blows down houses of straw and sticks.", "The Big Bad Wolf", "The Three Bears", "The Giant", "The Troll", "easy"),
]
for q, a, b, c, d, diff in fairy:
    put("Entertainment: Books", diff, q, a, b, c, d)

computers = [
("CPU stands for this.", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Core Processing Utility", "easy"),
("RAM stands for this.", "Random Access Memory", "Read Access Memory", "Rapid Action Module", "Remote Access Machine", "easy"),
("This language styles web pages.", "CSS", "HTML", "SQL", "PDF", "medium"),
("This markup language builds the structure of a web page.", "HTML", "CSS", "Python", "JPEG", "easy"),
("This key saves a document in many programs, with Control.", "S", "Z", "C", "V", "easy"),
("This key undoes an action in many programs, with Control.", "Z", "Y", "X", "U", "easy"),
("Wi-Fi is a way to connect without these.", "Cables", "Passwords", "Screens", "Batteries", "easy"),
]
for q, a, b, c, d, diff in computers:
    put("Science: Computers", diff, q, a, b, c, d)

more_geo = [
("This is the capital of France.", "Paris", "Lyon", "Marseille", "Nice", "easy"),
("This is the capital of the United Kingdom.", "London", "Manchester", "Edinburgh", "Birmingham", "easy"),
("This is the capital of Germany.", "Berlin", "Munich", "Frankfurt", "Hamburg", "easy"),
("This is the capital of Canada.", "Ottawa", "Toronto", "Montreal", "Vancouver", "medium"),
("This is the capital of Australia.", "Canberra", "Sydney", "Melbourne", "Perth", "medium"),
("This is the capital of Mexico.", "Mexico City", "Guadalajara", "Cancun", "Monterrey", "easy"),
("This is the capital of Egypt.", "Cairo", "Alexandria", "Giza", "Luxor", "easy"),
("This is the capital of China.", "Beijing", "Shanghai", "Hong Kong", "Guangzhou", "easy"),
("This is the capital of India.", "New Delhi", "Mumbai", "Kolkata", "Bangalore", "medium"),
("This is the capital of Russia.", "Moscow", "St. Petersburg", "Kazan", "Sochi", "easy"),
("This U.S. state has Austin as its capital.", "Texas", "California", "Florida", "Arizona", "easy"),
("This U.S. state has Sacramento as its capital.", "California", "Nevada", "Oregon", "Arizona", "medium"),
("This U.S. state has Albany as its capital.", "New York", "New Jersey", "Pennsylvania", "Massachusetts", "medium"),
("Mount Everest is the highest peak on this continent.", "Asia", "Europe", "Africa", "South America", "easy"),
("The Amazon River is on this continent.", "South America", "Africa", "Asia", "Australia", "easy"),
("The Nile flows through this continent.", "Africa", "Asia", "Europe", "South America", "easy"),
("This continent is also a country.", "Australia", "Antarctica", "Europe", "Africa", "medium"),
("This is the coldest continent.", "Antarctica", "Europe", "North America", "Asia", "easy"),
]
for q, a, b, c, d, diff in more_geo:
    put("Geography", diff, q, a, b, c, d)

more_hist = [
("This man wrote the Declaration of Independence.", "Thomas Jefferson", "John Adams", "Benjamin Franklin", "George Washington", "medium"),
("This man flew a kite in a thunderstorm in the famous story.", "Benjamin Franklin", "Thomas Edison", "Alexander Graham Bell", "Samuel Morse", "easy"),
("This woman refused to give up her bus seat in Montgomery.", "Rosa Parks", "Harriet Tubman", "Sojourner Truth", "Ida B. Wells", "easy"),
("This woman led many people north on the Underground Railroad.", "Harriet Tubman", "Rosa Parks", "Sojourner Truth", "Harriet Beecher Stowe", "medium"),
("This nurse worked in the Crimean War and is called the Lady with the Lamp.", "Florence Nightingale", "Clara Barton", "Mary Seacole", "Dorothea Dix", "hard"),
("This emperor of France was defeated at Waterloo.", "Napoleon", "Louis XIV", "Charlemagne", "Wellington", "medium"),
("This English queen defeated the Spanish Armada's era.", "Elizabeth I", "Victoria", "Mary I", "Anne", "medium"),
("This ancient Macedonian conquered a huge empire by age 30.", "Alexander the Great", "Julius Caesar", "Hannibal", "Darius", "medium"),
("This Roman leader was assassinated on the Ides of March.", "Julius Caesar", "Augustus", "Nero", "Marcus Aurelius", "medium"),
("This Egyptian queen allied with Caesar and Antony.", "Cleopatra", "Nefertiti", "Hatshepsut", "Nefertari", "easy"),
("This monk posted debates that sparked the Protestant Reformation.", "Martin Luther", "John Calvin", "Henry VIII", "Erasmus", "hard"),
("This king had six wives.", "Henry VIII", "Henry VII", "Richard III", "Charles I", "medium"),
("This ship brought the Pilgrims to Plymouth in 1620.", "The Mayflower", "The Santa Maria", "The Beagle", "The Golden Hind", "easy"),
("This pandemic in the 1300s is called the Black Death.", "The bubonic plague", "Smallpox", "Cholera", "Influenza", "medium"),
("This wall was built by a Roman emperor across northern Britain.", "Hadrian's Wall", "The Antonine Wall", "The Berlin Wall", "Offa's Dyke", "hard"),
]
for q, a, b, c, d, diff in more_hist:
    put("History", diff, q, a, b, c, d)

more_food = [
("This sauce is tomatoes cooked down and served on pasta.", "Marinara", "Alfredo", "Pesto", "Bolognese", "easy"),
("This pasta sauce is cream, butter, and cheese.", "Alfredo", "Marinara", "Pesto", "Arrabbiata", "easy"),
("Sushi wrapped in seaweed is called this.", "Maki", "Nigiri", "Sashimi", "Tempura", "medium"),
("Raw fish sliced without rice is called this.", "Sashimi", "Nigiri", "Maki", "Tempura", "medium"),
("This Japanese dish is battered and fried.", "Tempura", "Teriyaki", "Sashimi", "Miso", "easy"),
("This flatbread is cooked in a tandoor.", "Naan", "Pita", "Tortilla", "Focaccia", "medium"),
("This Mexican sauce is made from avocados.", "Guacamole", "Salsa", "Queso", "Mole", "easy"),
("This dip is chickpeas and tahini.", "Hummus", "Baba ganoush", "Tzatziki", "Tapenade", "easy"),
("Eggplant dip common in the Middle East is this.", "Baba ganoush", "Hummus", "Tzatziki", "Tabbouleh", "hard"),
("This breakfast meat comes from a pig's belly and is often crispy.", "Bacon", "Ham", "Sausage", "Prosciutto", "easy"),
("This Italian coffee is a small strong shot.", "Espresso", "Latte", "Cappuccino", "Americano", "easy"),
("This coffee drink is espresso with steamed milk and foam.", "Cappuccino", "Americano", "Espresso", "Cold brew", "easy"),
("This sparkling wine comes from a region in France.", "Champagne", "Prosecco", "Cava", "Lambrusco", "medium"),
("This spirit is distilled from agave.", "Tequila", "Rum", "Vodka", "Whiskey", "easy"),
("This spirit is distilled from sugarcane.", "Rum", "Tequila", "Gin", "Brandy", "medium"),
("This spirit is grain spirit flavored with juniper.", "Gin", "Vodka", "Whiskey", "Rum", "medium"),
]
for q, a, b, c, d, diff in more_food:
    put("Food & Drink", diff, q, a, b, c, d)

more_animals = [
("This reptile changes color and has a long tongue.", "A chameleon", "A gecko", "An iguana", "A skink", "easy"),
("This animal carries its home on its back.", "A turtle", "A crab", "A snail", "A tortoise", "easy"),
("This slow reptile is a turtle that lives on land.", "A tortoise", "A sea turtle", "A terrapin", "A newt", "medium"),
("This fish has a skeleton of cartilage and many teeth.", "A shark", "A tuna", "A salmon", "A swordfish", "easy"),
("This mammal flies using skin between its fingers.", "A bat", "A flying squirrel", "A sugar glider", "A bird", "easy"),
("This bird hoots and hunts at night.", "An owl", "A hawk", "An eagle", "A crow", "easy"),
("This pink bird stands on one leg in shallow water.", "A flamingo", "A stork", "A heron", "A crane", "easy"),
("This black bird is linked with the Tower of London.", "A raven", "A crow", "A magpie", "A jackdaw", "medium"),
("This pet rodent has a short tail and cheek pouches.", "A hamster", "A gerbil", "A mouse", "A rat", "easy"),
("This farm bird wakes people with a crow.", "A rooster", "A hen", "A turkey", "A goose", "easy"),
("This water bird is the male of the species that quacks.", "A drake", "A gander", "A cob", "A rooster", "hard"),
("This big cat has spots and is the fastest.", "A cheetah", "A leopard", "A jaguar", "A snow leopard", "easy"),
("This big cat has a mane.", "A lion", "A tiger", "A cougar", "A lynx", "easy"),
("This big cat has stripes.", "A tiger", "A zebra", "A leopard", "A cheetah", "easy"),
("This bear lives on Arctic ice.", "A polar bear", "A grizzly bear", "A black bear", "A panda", "easy"),
]
for q, a, b, c, d, diff in more_animals:
    put("Animals", diff, q, a, b, c, d)

directors = [
("Jaws", "Steven Spielberg"), ("E.T. the Extra-Terrestrial", "Steven Spielberg"),
("Jurassic Park", "Steven Spielberg"), ("Schindler's List", "Steven Spielberg"),
("The Godfather", "Francis Ford Coppola"), ("Apocalypse Now", "Francis Ford Coppola"),
("Pulp Fiction", "Quentin Tarantino"), ("Kill Bill", "Quentin Tarantino"),
("Inception", "Christopher Nolan"), ("The Dark Knight", "Christopher Nolan"),
("Titanic", "James Cameron"), ("Avatar", "James Cameron"),
("Get Out", "Jordan Peele"), ("Nope", "Jordan Peele"),
("Lady Bird", "Greta Gerwig"), ("Barbie", "Greta Gerwig"),
("The Shape of Water", "Guillermo del Toro"), ("Pan's Labyrinth", "Guillermo del Toro"),
]
dirs = []
for _, d in directors:
    if d not in dirs:
        dirs.append(d)
for film, director in directors:
    put("Entertainment: Film", "medium", f"This director made {film}.", director, *wrongs(dirs, director))

books2 = [
("Pride and Prejudice", "Jane Austen"), ("Emma", "Jane Austen"),
("Romeo and Juliet", "William Shakespeare"), ("Hamlet", "William Shakespeare"),
("Macbeth", "William Shakespeare"), ("A Midsummer Night's Dream", "William Shakespeare"),
("Oliver Twist", "Charles Dickens"), ("A Christmas Carol", "Charles Dickens"),
("Great Expectations", "Charles Dickens"),
("The Adventures of Huckleberry Finn", "Mark Twain"), ("The Adventures of Tom Sawyer", "Mark Twain"),
("Frankenstein", "Mary Shelley"), ("Dracula", "Bram Stoker"),
("The Great Gatsby", "F. Scott Fitzgerald"), ("To Kill a Mockingbird", "Harper Lee"),
("The Catcher in the Rye", "J.D. Salinger"), ("Of Mice and Men", "John Steinbeck"),
("The Grapes of Wrath", "John Steinbeck"), ("Beloved", "Toni Morrison"),
("The Handmaid's Tale", "Margaret Atwood"), ("The Hunger Games", "Suzanne Collins"),
("The Fault in Our Stars", "John Green"), ("Divergent", "Veronica Roth"),
("The Hobbit", "J.R.R. Tolkien"), ("The Lion, the Witch and the Wardrobe", "C.S. Lewis"),
("Matilda", "Roald Dahl"), ("Charlie and the Chocolate Factory", "Roald Dahl"),
("Charlotte's Web", "E.B. White"), ("The Very Hungry Caterpillar", "Eric Carle"),
("Where the Wild Things Are", "Maurice Sendak"), ("Goodnight Moon", "Margaret Wise Brown"),
]
authors = []
for _, a in books2:
    if a not in authors:
        authors.append(a)
for book, author in books2:
    put("Entertainment: Books", "medium", f"This author wrote {book}.", author, *wrongs(authors, author))

shows = [
("Ross Geller", "Friends"), ("Rachel Green", "Friends"), ("Monica Geller", "Friends"),
("Chandler Bing", "Friends"), ("Joey Tribbiani", "Friends"), ("Phoebe Buffay", "Friends"),
("Michael Scott", "The Office"), ("Dwight Schrute", "The Office"), ("Jim Halpert", "The Office"),
("Pam Beesly", "The Office"), ("Kelly Kapoor", "The Office"),
("Jerry Seinfeld", "Seinfeld"), ("George Costanza", "Seinfeld"), ("Elaine Benes", "Seinfeld"),
("Cosmo Kramer", "Seinfeld"),
("Homer Simpson", "The Simpsons"), ("Marge Simpson", "The Simpsons"),
("Bart Simpson", "The Simpsons"), ("Lisa Simpson", "The Simpsons"),
("Walter White", "Breaking Bad"), ("Jesse Pinkman", "Breaking Bad"),
("Saul Goodman", "Breaking Bad"), ("Skyler White", "Breaking Bad"),
("Eleven", "Stranger Things"), ("Mike Wheeler", "Stranger Things"),
("Dustin Henderson", "Stranger Things"), ("Lucas Sinclair", "Stranger Things"),
("Jim Hopper", "Stranger Things"),
("Jon Snow", "Game of Thrones"), ("Daenerys Targaryen", "Game of Thrones"),
("Tyrion Lannister", "Game of Thrones"), ("Arya Stark", "Game of Thrones"),
("Cersei Lannister", "Game of Thrones"),
("Leslie Knope", "Parks and Recreation"), ("Ron Swanson", "Parks and Recreation"),
("Ted Lasso", "Ted Lasso"), ("Roy Kent", "Ted Lasso"),
]
show_names = []
for _, s in shows:
    if s not in show_names:
        show_names.append(s)
for person, show in shows:
    put("Entertainment: Television", "easy", f"{person} is a character on this show.", show, *wrongs(show_names, show))

games2 = [
("Mario", "Super Mario Bros."), ("Link", "The Legend of Zelda"),
("Pikachu", "Pokemon"), ("Sonic", "Sonic the Hedgehog"),
("Master Chief", "Halo"), ("Kratos", "God of War"),
("Lara Croft", "Tomb Raider"), ("Solid Snake", "Metal Gear Solid"),
("Cloud Strife", "Final Fantasy VII"), ("Geralt", "The Witcher"),
("Arthur Morgan", "Red Dead Redemption 2"), ("Nathan Drake", "Uncharted"),
("Aloy", "Horizon Zero Dawn"), ("Ellie", "The Last of Us"),
("Joel", "The Last of Us"), ("Steve", "Minecraft"),
("Crash Bandicoot", "Crash Bandicoot"), ("Spyro", "Spyro the Dragon"),
("Kirby", "Kirby's Dream Land"), ("Samus Aran", "Metroid"),
]
gn = []
for _, g in games2:
    if g not in gn:
        gn.append(g)
for hero, game in games2:
    put("Entertainment: Video Games", "medium", f"{hero} is the hero of this game.", game, *wrongs(gn, game))

myth2 = [
("The god of war in Greek myth is this.", "Ares", "Athena", "Apollo", "Hephaestus", "medium"),
("The goddess of wisdom in Greek myth is this.", "Athena", "Hera", "Aphrodite", "Artemis", "medium"),
("The goddess of love in Greek myth is this.", "Aphrodite", "Athena", "Hera", "Persephone", "easy"),
("The god of the sun in Greek myth is this.", "Apollo", "Helios", "Hermes", "Ares", "medium"),
("The goddess of the hunt in Greek myth is this.", "Artemis", "Athena", "Demeter", "Hestia", "medium"),
("The queen of the Greek gods is this.", "Hera", "Hestia", "Demeter", "Aphrodite", "easy"),
("The god of the forge in Greek myth is this.", "Hephaestus", "Ares", "Hermes", "Dionysus", "hard"),
("The god of wine in Greek myth is this.", "Dionysus", "Apollo", "Pan", "Hermes", "medium"),
("The Roman name for Zeus is this.", "Jupiter", "Mars", "Neptune", "Mercury", "medium"),
("The Roman name for Poseidon is this.", "Neptune", "Pluto", "Mars", "Jupiter", "medium"),
("The Roman name for Hades is this.", "Pluto", "Neptune", "Mars", "Vulcan", "medium"),
("The Roman name for Ares is this.", "Mars", "Mercury", "Jupiter", "Saturn", "easy"),
]
for q, a, b, c, d, diff in myth2:
    put("Mythology", diff, q, a, b, c, d)

art2 = [
("This artist cut off part of his own ear.", "Vincent van Gogh", "Paul Gauguin", "Claude Monet", "Edgar Degas", "medium"),
("This artist sculpted David.", "Michelangelo", "Donatello", "Bernini", "Rodin", "medium"),
("This artist painted Guernica.", "Pablo Picasso", "Salvador Dali", "Joan Miro", "Francisco Goya", "hard"),
("This artist painted American Gothic.", "Grant Wood", "Edward Hopper", "Norman Rockwell", "Andrew Wyeth", "hard"),
("This artist painted Nighthawks.", "Edward Hopper", "Grant Wood", "Norman Rockwell", "Georgia O'Keeffe", "hard"),
("This artist is known for large flowers of the American Southwest.", "Georgia O'Keeffe", "Frida Kahlo", "Mary Cassatt", "Berthe Morisot", "medium"),
("This Mexican artist painted many self-portraits with a unibrow.", "Frida Kahlo", "Diego Rivera", "Georgia O'Keeffe", "Remedios Varo", "medium"),
("This artist painted the ceiling mural The Creation of Adam.", "Michelangelo", "Raphael", "Leonardo da Vinci", "Titian", "medium"),
]
for q, a, b, c, d, diff in art2:
    put("Art", diff, q, a, b, c, d)

holidays = [
("This November holiday in the U.S. centers on a feast.", "Thanksgiving", "Halloween", "Labor Day", "Memorial Day", "easy"),
("This October holiday features costumes.", "Halloween", "Thanksgiving", "Christmas", "Easter", "easy"),
("This spring holiday uses eggs and baskets.", "Easter", "Christmas", "Halloween", "Passover", "easy"),
("This winter holiday uses a tree and gifts for many families.", "Christmas", "Hanukkah", "Kwanzaa", "New Year's Eve", "easy"),
("This festival of lights lasts eight nights.", "Hanukkah", "Diwali", "Kwanzaa", "Christmas", "medium"),
("This Indian festival of lights uses lamps called diyas.", "Diwali", "Holi", "Hanukkah", "Eid", "medium"),
("This holiday marks the new year on January 1.", "New Year's Day", "Christmas", "Epiphany", "Labor Day", "easy"),
]
for q, a, b, c, d, diff in holidays:
    put("General Knowledge", diff, q, a, b, c, d)
