"""Write original clue-style questions, then stop. Run once."""
from pathlib import Path

# category, difficulty, question, correct, wrong, wrong, wrong
ROWS = []

def add(cat, diff, q, a, b, c, d):
    ROWS.append((cat, diff, q, a, b, c, d))

# --- Film ---
film = [
("easy", "The wizard school in the Harry Potter films is this castle.", "Hogwarts", "Durmstrang", "Beauxbatons", "Ilvermorny"),
("easy", "This 1997 film follows a romance aboard a famous ocean liner.", "Titanic", "Poseidon", "The Perfect Storm", "Cast Away"),
("easy", "A lion cub named Simba is the hero of this Disney movie.", "The Lion King", "Bambi", "Tarzan", "The Jungle Book"),
("easy", "This green ogre lives in a swamp in a popular animated film.", "Shrek", "Hulk", "Mike Wazowski", "Sulley"),
("easy", "Woody and Buzz Lightyear are toys in this Pixar movie.", "Toy Story", "Cars", "Finding Nemo", "Up"),
("easy", "May the Force be with you is a line from this movie series.", "Star Wars", "Star Trek", "Dune", "Avatar"),
("easy", "This superhero is known as the Dark Knight.", "Batman", "Superman", "Spider-Man", "Iron Man"),
("easy", "Dorothy travels to Oz in this classic film.", "The Wizard of Oz", "Mary Poppins", "Willy Wonka and the Chocolate Factory", "Chitty Chitty Bang Bang"),
("easy", "A clownfish named Nemo gets lost in this Pixar movie.", "Finding Nemo", "Shark Tale", "The Little Mermaid", "Moana"),
("easy", "Elsa sings Let It Go in this Disney film.", "Frozen", "Tangled", "Moana", "Encanto"),
("easy", "This Marvel hero is a billionaire in a metal suit.", "Iron Man", "Black Panther", "Thor", "Ant-Man"),
("easy", "This friendly alien just wants to phone home.", "E.T.", "Alien", "Paul", "Mac"),
("easy", "Kevin McCallister defends his house in this Christmas comedy.", "Home Alone", "Elf", "The Santa Clause", "Jingle All the Way"),
("easy", "Sylvester Stallone plays a boxer named Rocky in this film series.", "Rocky", "Raging Bull", "Creed", "The Fighter"),
("easy", "A great white shark terrorizes a beach town in this 1975 film.", "Jaws", "Deep Blue Sea", "The Meg", "Open Water"),
("easy", "Dinosaurs are cloned on an island in this film series.", "Jurassic Park", "King Kong", "Godzilla", "Land of the Lost"),
("easy", "The blue Na'vi live on this moon in Avatar.", "Pandora", "Tatooine", "Arrakis", "Endor"),
("easy", "T'Challa rules this Marvel nation.", "Wakanda", "Latveria", "Asgard", "Genosha"),
("easy", "A bite from a radioactive spider creates this hero.", "Spider-Man", "Ant-Man", "Blue Beetle", "Nightwing"),
("easy", "This god of thunder wields a hammer named Mjolnir.", "Thor", "Loki", "Odin", "Zeus"),
("easy", "This pirate captain is played by Johnny Depp.", "Jack Sparrow", "Hector Barbossa", "Will Turner", "Davy Jones"),
("easy", "Buzz Lightyear's catchphrase is about infinity and this.", "Beyond", "Tomorrow", "Forever", "Always"),
("easy", "This snowman sings about summer in Frozen.", "Olaf", "Marshmallow", "Kristoff", "Sven"),
("easy", "This cowboy doll is the leader of Andy's toys.", "Woody", "Jessie", "Bullseye", "Rex"),
("easy", "This space ranger toy thinks he is a real space ranger.", "Buzz Lightyear", "Woody", "Emperor Zurg", "Bo Peep"),
("medium", "This 1994 film follows Forrest through decades of American life.", "Forrest Gump", "Big", "The Truman Show", "Cast Away"),
("medium", "Neo chooses the red pill in this science-fiction film.", "The Matrix", "Inception", "Dark City", "The Thirteenth Floor"),
("medium", "Don Vito Corleone is the patriarch in this crime saga.", "The Godfather", "Goodfellas", "Scarface", "Casino"),
("medium", "A DeLorean is the time machine in this 1985 comedy.", "Back to the Future", "Bill and Ted's Excellent Adventure", "Hot Tub Time Machine", "Looper"),
("medium", "Who you gonna call is the slogan of this comedy.", "Ghostbusters", "Beetlejuice", "Gremlins", "Men in Black"),
("medium", "A lonely robot cleans an empty Earth in this Pixar film.", "WALL-E", "Robots", "Big Hero 6", "Astro Boy"),
("medium", "An old man lifts his house with balloons in this Pixar film.", "Up", "Brave", "Coco", "Soul"),
("medium", "Joy, Sadness, and Anger live in a girl's mind in this Pixar film.", "Inside Out", "Soul", "Turning Red", "Luca"),
("medium", "Miguel visits the Land of the Dead in this Pixar film.", "Coco", "Encanto", "The Book of Life", "Corpse Bride"),
("medium", "This Disney musical is set in the kingdom of Arendelle.", "Frozen", "Tangled", "Brave", "Moana"),
("medium", "A rat named Remy cooks in a Paris restaurant in this Pixar film.", "Ratatouille", "Flushed Away", "The Secret of NIMH", "Stuart Little"),
("medium", "Lightning McQueen is a race car in this Pixar film.", "Cars", "Turbo", "Speed Racer", "Herbie"),
("medium", "Monsters scare children to power their city in this Pixar film.", "Monsters, Inc.", "Hotel Transylvania", "Monsters vs. Aliens", "Frankenweenie"),
("medium", "A family of superheroes hides in the suburbs in this Pixar film.", "The Incredibles", "Sky High", "Fantastic Four", "Big Hero 6"),
("medium", "This 1999 film popularized bullet time.", "The Matrix", "John Wick", "Equilibrium", "Wanted"),
("medium", "This film's quote is Here's looking at you, kid.", "Casablanca", "Gone with the Wind", "Citizen Kane", "Rebecca"),
("medium", "Atticus Finch defends a man in court in this 1962 film.", "To Kill a Mockingbird", "12 Angry Men", "Inherit the Wind", "Judgment at Nuremberg"),
("medium", "This western features a standoff at high noon in the title.", "High Noon", "Shane", "Rio Bravo", "Unforgiven"),
("hard", "This 1941 film is famous for the word Rosebud.", "Citizen Kane", "Casablanca", "The Maltese Falcon", "Sunset Boulevard"),
("hard", "This Best Picture winner is about a silent-film star moving into talkies.", "The Artist", "La La Land", "Singin' in the Rain", "Birdman"),
("hard", "This 1975 Best Picture follows a mental patient and a rebellious newcomer.", "One Flew Over the Cuckoo's Nest", "The Shining", "Awakenings", "Girl, Interrupted"),
("hard", "This Coen brothers film follows a man who loses a briefcase of money.", "Fargo", "No Country for Old Men", "The Big Lebowski", "Burn After Reading"),
("hard", "A hit man and a boxer share a night in this Tarantino film.", "Pulp Fiction", "Reservoir Dogs", "Jackie Brown", "Kill Bill"),
("hard", "This 2001 musical was filmed in the Moulin Rouge in Paris in the story.", "Moulin Rouge!", "Chicago", "Cabaret", "The Phantom of the Opera"),
]
for row in film:
    add("Entertainment: Film", *row)

root = Path(__file__).resolve().parent
for extra in sorted(root.glob("clue_pack_*.py")):
    namespace = {}
    exec(extra.read_text(encoding="utf-8"), namespace)
    for row in namespace["ROWS"]:
        if row[3].lower() in row[2].lower():
            continue
        add(*row)

out = root / "clue_style_01.txt"
lines = ["|".join(row) for row in ROWS]
# validate
for i, line in enumerate(lines, 1):
    parts = line.split("|")
    if len(parts) != 7:
        raise SystemExit(f"bad {i}")
    if len({p.lower() for p in parts[3:]}) != 4:
        raise SystemExit(f"dup choice {i}: {line}")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(len(lines))
