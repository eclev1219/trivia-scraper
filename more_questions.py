"""Add a batch of original trivia questions and drop leftover fact fields."""

import json
import os

DATABASE_FILE = "questions.json"

# category, difficulty, question, correct answer, three wrong answers
QUESTIONS = [
    ("Art", "easy", "Who painted the Mona Lisa?", "Leonardo da Vinci", ["Michelangelo", "Raphael", "Titian"]),
    ("Art", "easy", "Who painted The Starry Night?", "Vincent van Gogh", ["Claude Monet", "Paul Cezanne", "Edvard Munch"]),
    ("Art", "easy", "Who sculpted the marble statue of David in Florence?", "Michelangelo", ["Donatello", "Bernini", "Rodin"]),
    ("Art", "medium", "Who painted Guernica?", "Pablo Picasso", ["Salvador Dali", "Joan Miro", "Diego Rivera"]),
    ("Art", "medium", "Who painted The Persistence of Memory, with its melting clocks?", "Salvador Dali", ["Rene Magritte", "Max Ernst", "Frida Kahlo"]),
    ("Art", "medium", "Who painted Girl with a Pearl Earring?", "Johannes Vermeer", ["Rembrandt", "Frans Hals", "Jan Steen"]),
    ("Art", "easy", "Who painted The Scream?", "Edvard Munch", ["Gustav Klimt", "Egon Schiele", "Wassily Kandinsky"]),
    ("Art", "medium", "Who painted American Gothic?", "Grant Wood", ["Edward Hopper", "Norman Rockwell", "Andrew Wyeth"]),
    ("Art", "medium", "Who painted Nighthawks?", "Edward Hopper", ["Georgia O'Keeffe", "Stuart Davis", "Thomas Hart Benton"]),
    ("Art", "medium", "Impression, Sunrise, the painting that gave Impressionism its name, was painted by whom?", "Claude Monet", ["Pierre-Auguste Renoir", "Edgar Degas", "Camille Pissarro"]),
    ("Art", "medium", "Who painted the Campbell's Soup Cans?", "Andy Warhol", ["Roy Lichtenstein", "Jasper Johns", "Keith Haring"]),
    ("Art", "easy", "Who sculpted The Thinker?", "Auguste Rodin", ["Henry Moore", "Constantin Brancusi", "Alberto Giacometti"]),
    ("Art", "medium", "Who painted The Birth of Venus?", "Sandro Botticelli", ["Leonardo da Vinci", "Raphael", "Titian"]),
    ("Art", "medium", "Who painted The Night Watch?", "Rembrandt", ["Johannes Vermeer", "Peter Paul Rubens", "Anthony van Dyck"]),
    ("Art", "hard", "Who painted Las Meninas?", "Diego Velazquez", ["El Greco", "Francisco Goya", "Bartolome Esteban Murillo"]),
    ("Art", "medium", "Who painted The Kiss, with its gold-leaf couple?", "Gustav Klimt", ["Egon Schiele", "Alphonse Mucha", "Gustav Moreau"]),
    ("Mythology", "easy", "In Greek myth, who is the king of the gods?", "Zeus", ["Poseidon", "Hades", "Apollo"]),
    ("Mythology", "easy", "In Norse myth, what is the name of Thor's hammer?", "Mjolnir", ["Gungnir", "Gram", "Hofund"]),
    ("Mythology", "medium", "In Norse myth, what is the great tree that connects the worlds?", "Yggdrasil", ["Ratatoskr", "Bifrost", "Valhalla"]),
    ("Mythology", "medium", "In Shinto tradition, who is the sun goddess?", "Amaterasu", ["Susanoo", "Tsukuyomi", "Izanami"]),
    ("Mythology", "medium", "Quetzalcoatl, the feathered serpent, belongs to the mythology of which region?", "Mesoamerica", ["Ancient Egypt", "Norse Scandinavia", "Polynesia"]),
    ("Mythology", "medium", "Anansi the spider is a trickster in the stories of which region?", "West Africa", ["Ancient Greece", "Japan", "The Andes"]),
    ("Mythology", "easy", "In Greek myth, who is the goddess of wisdom?", "Athena", ["Aphrodite", "Hera", "Artemis"]),
    ("Mythology", "medium", "In Egyptian myth, who is the god associated with the sun?", "Ra", ["Osiris", "Anubis", "Set"]),
    ("Mythology", "medium", "In Greek myth, who must spend part of each year in the underworld, a story tied to the seasons?", "Persephone", ["Ariadne", "Atalanta", "Medea"]),
    ("Mythology", "easy", "In Greek myth, who slays the Minotaur?", "Theseus", ["Perseus", "Heracles", "Jason"]),
    ("Mythology", "easy", "The Trojan Horse was used to enter which city?", "Troy", ["Sparta", "Athens", "Carthage"]),
    ("Mythology", "medium", "In Norse myth, Valhalla is the hall of which god?", "Odin", ["Thor", "Loki", "Freyr"]),
    ("Mythology", "medium", "In the Epic of Gilgamesh, Gilgamesh is king of which city?", "Uruk", ["Babylon", "Nineveh", "Memphis"]),
    ("Mythology", "medium", "Sun Wukong, the Monkey King, is a central character in which story?", "Journey to the West", ["The Tale of Genji", "The Ramayana", "The Popol Vuh"]),
    ("Mythology", "hard", "In Polynesian stories, who fishes islands from the sea and slows the sun?", "Maui", ["Pele", "Tangaroa", "Tane"]),
    ("Mythology", "medium", "In Hindu tradition, who is the god of destruction and transformation in the Trimurti?", "Shiva", ["Brahma", "Vishnu", "Indra"]),
    ("Animals", "easy", "What is the largest animal alive today?", "Blue whale", ["African bush elephant", "Whale shark", "Giraffe"]),
    ("Animals", "easy", "What is the fastest land animal over a short sprint?", "Cheetah", ["Pronghorn", "Lion", "Ostrich"]),
    ("Animals", "medium", "Which bird is the fastest animal in a hunting dive?", "Peregrine falcon", ["Golden eagle", "Swift", "Albatross"]),
    ("Animals", "easy", "What is the largest living species of penguin?", "Emperor penguin", ["King penguin", "Adelie penguin", "Gentoo penguin"]),
    ("Animals", "medium", "Which bird migrates from the Arctic to the Antarctic and back each year?", "Arctic tern", ["Wandering albatross", "Barn swallow", "Canada goose"]),
    ("Animals", "medium", "A narwhal's tusk is actually what?", "A tooth", ["A horn of bone", "A hardened fin", "A beak"]),
    ("Animals", "easy", "What is the largest living rodent?", "Capybara", ["Beaver", "Porcupine", "Nutria"]),
    ("Animals", "medium", "The axolotl, a salamander that keeps its larval gills as an adult, is native to which country?", "Mexico", ["Japan", "Australia", "Brazil"]),
    ("Animals", "medium", "The okapi's closest living relative is which animal?", "Giraffe", ["Zebra", "Deer", "Tapir"]),
    ("Animals", "hard", "What is the largest carnivorous mammal native to Madagascar?", "Fossa", ["Lemur", "Aye-aye", "Tenrec"]),
    ("Animals", "easy", "What is the largest living lizard?", "Komodo dragon", ["Nile monitor", "Gila monster", "Iguana"]),
    ("Animals", "easy", "Which of these mammals lays eggs?", "Platypus", ["Kangaroo", "Bat", "Dolphin"]),
    ("Animals", "medium", "Leafcutter ants carry leaves mainly in order to do what?", "Grow fungus for food", ["Build waterproof nests", "Feed the leaves to their larvae", "Line their tunnels against rain"]),
    ("Animals", "medium", "A pistol shrimp stuns prey with what?", "A bubble from a snapping claw", ["An electric shock", "A spray of ink", "A venomous spine"]),
    ("Animals", "hard", "Which fish shoots a jet of water to knock insects into the water?", "Archerfish", ["Mudskipper", "Pufferfish", "Anglerfish"]),
    ("Animals", "medium", "The electric eel is most closely grouped with which animals?", "Knifefish", ["True eels", "Catfish", "Lampreys"]),
    ("Animals", "medium", "Which flightless parrot is native to New Zealand?", "Kakapo", ["Kiwi", "Takahe", "Kea"]),
    ("Animals", "hard", "The coelacanth, found alive in 1938, belongs to which group?", "Lobe-finned fish", ["Sharks", "Ray-finned fish", "Jawless fish"]),
    ("Animals", "medium", "Horseshoe crabs are valued in medicine because their blood is used to do what?", "Test for bacterial contamination", ["Clot human blood", "Treat malaria", "Make blue dye"]),
    ("Science & Nature", "easy", "What is the closest star to Earth after the Sun?", "Proxima Centauri", ["Sirius", "Alpha Centauri A", "Betelgeuse"]),
    ("Science & Nature", "easy", "Which planet is the largest in the solar system?", "Jupiter", ["Saturn", "Neptune", "Uranus"]),
    ("Science & Nature", "medium", "Which planet has the hottest surface?", "Venus", ["Mercury", "Mars", "Jupiter"]),
    ("Science & Nature", "medium", "Which planet's average density is low enough that it would float in water?", "Saturn", ["Jupiter", "Neptune", "Uranus"]),
    ("Science & Nature", "medium", "Olympus Mons, the largest volcano in the solar system, is on which body?", "Mars", ["Venus", "Io", "The Moon"]),
    ("Science & Nature", "easy", "What is the deepest known point in the ocean?", "Challenger Deep", ["Tonga Trench", "Puerto Rico Trench", "Java Trench"]),
    ("Science & Nature", "medium", "What is the deepest lake in the world?", "Lake Baikal", ["Lake Tanganyika", "Crater Lake", "The Caspian Sea"]),
    ("Science & Nature", "easy", "What gas makes up most of Earth's atmosphere?", "Nitrogen", ["Oxygen", "Carbon dioxide", "Argon"]),
    ("Science & Nature", "medium", "What is the most abundant chemical element in the universe?", "Hydrogen", ["Helium", "Oxygen", "Carbon"]),
    ("Science & Nature", "medium", "What is the most abundant element in Earth's crust?", "Oxygen", ["Silicon", "Iron", "Aluminum"]),
    ("Science & Nature", "easy", "Diamond and graphite are both forms of which element?", "Carbon", ["Silicon", "Calcium", "Sulfur"]),
    ("Science & Nature", "medium", "The ozone layer that absorbs much of the Sun's ultraviolet light is in which atmospheric layer?", "Stratosphere", ["Troposphere", "Mesosphere", "Thermosphere"]),
    ("Science & Nature", "medium", "Who proposed the idea of continental drift?", "Alfred Wegener", ["Charles Lyell", "James Hutton", "Marie Tharp"]),
    ("Science & Nature", "easy", "About how fast is light in a vacuum?", "300,000 kilometers per second", ["300 kilometers per second", "3,000 kilometers per second", "30,000 kilometers per second"]),
    ("Science & Nature", "medium", "Halley's Comet returns about how often?", "Every 76 years", ["Every 12 years", "Every 200 years", "Every 26 years"]),
    ("Science & Nature", "medium", "In what year did the International Astronomical Union reclassify Pluto as a dwarf planet?", "2006", ["1999", "2015", "1980"]),
    ("Science & Nature", "easy", "Which organ produces insulin?", "Pancreas", ["Liver", "Kidney", "Thyroid"]),
    ("Science & Nature", "easy", "A shortage of which vitamin causes scurvy?", "Vitamin C", ["Vitamin D", "Vitamin A", "Vitamin K"]),
    ("Science & Nature", "medium", "About how many bones are in a typical adult human skeleton?", "206", ["180", "260", "312"]),
    ("Science & Nature", "medium", "Whose X-ray photograph of DNA, known as Photo 51, was crucial evidence for the double helix?", "Rosalind Franklin", ["Marie Curie", "Barbara McClintock", "Dorothy Hodgkin"]),
    ("Science & Nature", "easy", "Who published the first widely recognized periodic table in 1869?", "Dmitri Mendeleev", ["John Dalton", "Antoine Lavoisier", "Niels Bohr"]),
    ("Science & Nature", "easy", "Who discovered penicillin in 1928?", "Alexander Fleming", ["Louis Pasteur", "Joseph Lister", "Robert Koch"]),
    ("Science & Nature", "medium", "The World Health Organization certified that which disease had been eradicated in 1980?", "Smallpox", ["Polio", "Measles", "Malaria"]),
    ("Science & Nature", "medium", "Who was the first person to win two Nobel Prizes?", "Marie Curie", ["Linus Pauling", "John Bardeen", "Frederick Sanger"]),
    ("Science & Nature", "medium", "Antibiotics are effective against which of these?", "Bacteria", ["Viruses", "Prions", "All microbes equally"]),
    ("Science: Mathematics", "easy", "In a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides. What is this rule called?", "The Pythagorean theorem", ["The binomial theorem", "Fermat's Last Theorem", "The fundamental theorem of calculus"]),
    ("Science: Mathematics", "easy", "What is pi?", "The ratio of a circle's circumference to its diameter", ["The ratio of a circle's area to its radius", "The square root of 2", "The base of the natural logarithm"]),
    ("Science: Mathematics", "medium", "In ordinary flat geometry, the angles of a triangle add up to how many degrees?", "180", ["90", "360", "270"]),
    ("Science: Mathematics", "medium", "What is the decimal value of the binary number 1010?", "10", ["12", "8", "5"]),
    ("Science: Mathematics", "easy", "A gross is equal to how many items?", "144", ["100", "120", "64"]),
    ("Science: Mathematics", "medium", "A googol is 10 raised to what power?", "100", ["1,000", "10", "1,000,000"]),
    ("Science: Mathematics", "hard", "Euclid proved that there are how many prime numbers?", "Infinitely many", ["Exactly 100", "Finitely many, but the count is unknown", "Exactly one for each even number"]),
    ("Science: Mathematics", "medium", "In the Fibonacci sequence, each number is the sum of what?", "The two numbers before it", ["The number before it and 1", "All the numbers before it", "The number before it multiplied by 2"]),
    ("History", "easy", "In what year did the Battle of Hastings take place?", "1066", ["1215", "1415", "1666"]),
    ("History", "medium", "The Visigoths under Alaric sacked Rome in what year?", "410", ["476", "27 BCE", "1453"]),
    ("History", "medium", "Constantinople fell to the Ottoman Empire in what year?", "1453", ["1492", "1204", "1683"]),
    ("History", "easy", "Johannes Gutenberg is famous for developing what in Europe?", "The movable-type printing press", ["The mechanical clock", "The magnetic compass", "The telescope"]),
    ("History", "medium", "The Rosetta Stone was the key to reading which writing system?", "Egyptian hieroglyphs", ["Cuneiform", "Linear B", "Mayan glyphs"]),
    ("History", "medium", "The Peace of Westphalia, ending the Thirty Years' War, was signed in what year?", "1648", ["1618", "1713", "1555"]),
    ("History", "easy", "On what date is Bastille Day, marking the 1789 storming of the Bastille?", "July 14", ["July 4", "May 5", "August 10"]),
    ("History", "medium", "Napoleon was finally defeated at Waterloo in what year?", "1815", ["1805", "1799", "1821"]),
    ("History", "medium", "The United States bought the Louisiana Territory from which country?", "France", ["Spain", "Britain", "Mexico"]),
    ("History", "medium", "The Emancipation Proclamation took effect in what year?", "1863", ["1861", "1865", "1870"]),
    ("History", "medium", "The Meiji Restoration, which restored imperial rule in Japan, began in what year?", "1868", ["1853", "1895", "1912"]),
    ("History", "medium", "The Suez Canal opened in what year?", "1869", ["1914", "1830", "1889"]),
    ("History", "hard", "The Berlin Conference of 1884-1885 is associated with what?", "European claims to African territory", ["The end of the Franco-Prussian War", "The founding of the United Nations", "The partition of the Ottoman Empire"]),
    ("History", "medium", "D-Day, the Allied landing in Normandy, was on what date?", "June 6, 1944", ["May 8, 1945", "December 7, 1941", "September 1, 1939"]),
    ("History", "medium", "The first atomic bomb used in war was dropped on Hiroshima on what date?", "August 6, 1945", ["August 9, 1945", "July 16, 1945", "May 8, 1945"]),
    ("History", "medium", "The Cuban Missile Crisis took place in what year?", "1962", ["1950", "1968", "1979"]),
    ("History", "easy", "The Chernobyl nuclear accident happened in what year?", "1986", ["1979", "1991", "1984"]),
    ("History", "medium", "The Soviet Union was formally dissolved in what year?", "1991", ["1989", "1993", "1985"]),
    ("History", "medium", "Nelson Mandela was inaugurated as South Africa's president in what year?", "1994", ["1990", "1986", "1999"]),
    ("History", "medium", "The US Supreme Court decision Brown v. Board of Education was issued in what year?", "1954", ["1896", "1964", "1948"]),
    ("History", "hard", "The Seneca Falls Convention, an early US women's rights meeting, was held in what year?", "1848", ["1776", "1920", "1869"]),
    ("History", "medium", "Who led the Ming dynasty voyages of the treasure fleet?", "Zheng He", ["Kublai Khan", "Marco Polo", "Ibn Battuta"]),
    ("History", "medium", "Mansa Musa was the emperor of which West African empire?", "Mali", ["Ghana", "Songhai", "Benin"]),
    ("History", "medium", "Hatshepsut is famous as what?", "A woman who ruled Egypt as pharaoh", ["The last queen of Carthage", "A Greek philosopher", "The founder of the Mauryan Empire"]),
    ("History", "hard", "Boudica led a revolt against Roman rule in which region?", "Britain", ["Gaul", "Judea", "Egypt"]),
    ("History", "medium", "The best-known surviving sections of the Great Wall of China were largely built during which dynasty?", "Ming", ["Qin", "Han", "Tang"]),
    ("History", "medium", "The Mexican Revolution began in 1910 against which long-ruling president?", "Porfirio Diaz", ["Benito Juarez", "Santa Anna", "Pancho Villa"]),
    ("History", "medium", "The March on Washington, where Martin Luther King Jr. gave the 'I Have a Dream' speech, was in what year?", "1963", ["1955", "1968", "1965"]),
    ("Geography", "easy", "What is the capital of Australia?", "Canberra", ["Sydney", "Melbourne", "Perth"]),
    ("Geography", "easy", "What is the capital of Brazil?", "Brasilia", ["Rio de Janeiro", "Sao Paulo", "Salvador"]),
    ("Geography", "medium", "What is the capital of Kazakhstan?", "Astana", ["Almaty", "Tashkent", "Bishkek"]),
    ("Geography", "easy", "What is the largest country by land area?", "Russia", ["Canada", "China", "United States"]),
    ("Geography", "easy", "What is the smallest independent state by area?", "Vatican City", ["Monaco", "San Marino", "Nauru"]),
    ("Geography", "medium", "As of 2024, which country has the largest population?", "India", ["China", "United States", "Indonesia"]),
    ("Geography", "medium", "What is the highest mountain in North America?", "Denali", ["Mount Logan", "Pico de Orizaba", "Mount Whitney"]),
    ("Geography", "medium", "What is the highest mountain in South America?", "Aconcagua", ["Huascaran", "Chimborazo", "Cotopaxi"]),
    ("Geography", "easy", "What is the highest mountain in Africa?", "Kilimanjaro", ["Mount Kenya", "Ras Dashen", "Atlas Mountains"]),
    ("Geography", "medium", "What is the highest peak on the Australian mainland?", "Mount Kosciuszko", ["Uluru", "Mount Wellington", "Puncak Jaya"]),
    ("Geography", "medium", "What is the longest continental mountain range?", "The Andes", ["The Rockies", "The Himalayas", "The Alps"]),
    ("Geography", "medium", "What is the longest river in the United States?", "The Missouri", ["The Mississippi", "The Yukon", "The Colorado"]),
    ("Geography", "medium", "What is the longest river in Asia?", "The Yangtze", ["The Ganges", "The Mekong", "The Yellow River"]),
    ("Geography", "easy", "The Amazon River is the world's largest by what measure?", "Volume of water", ["Number of bridges", "Depth", "Width of its delta"]),
    ("Geography", "medium", "Angel Falls, the world's highest uninterrupted waterfall, is in which country?", "Venezuela", ["Brazil", "South Africa", "Norway"]),
    ("Geography", "medium", "Victoria Falls is on the border of Zambia and which country?", "Zimbabwe", ["Botswana", "Mozambique", "Namibia"]),
    ("Geography", "easy", "The Suez Canal connects the Mediterranean Sea to which body of water?", "The Red Sea", ["The Persian Gulf", "The Black Sea", "The Arabian Sea"]),
    ("Geography", "easy", "The Panama Canal connects the Atlantic Ocean to which ocean?", "The Pacific Ocean", ["The Indian Ocean", "The Arctic Ocean", "The Southern Ocean"]),
    ("Geography", "medium", "The Bosporus connects the Black Sea to which sea?", "The Sea of Marmara", ["The Adriatic Sea", "The Aegean Sea", "The Caspian Sea"]),
    ("Geography", "medium", "The Strait of Gibraltar separates Europe from which continent?", "Africa", ["Asia", "North America", "South America"]),
    ("Geography", "easy", "The prime meridian passes through which place?", "Greenwich", ["Paris", "Quito", "Cairo"]),
    ("Geography", "medium", "The shore of the Dead Sea is notable as what?", "Earth's lowest land elevation", ["The saltiest water in the solar system", "The deepest lake", "The source of the Nile"]),
    ("Geography", "medium", "The Atacama Desert, one of the driest places on Earth, is mainly in which country?", "Chile", ["Morocco", "Australia", "Mongolia"]),
    ("Geography", "medium", "Including its overseas territories, which country uses the most time zones?", "France", ["Russia", "United States", "United Kingdom"]),
    ("Entertainment: Books", "easy", "Who wrote 1984?", "George Orwell", ["Aldous Huxley", "Ray Bradbury", "H. G. Wells"]),
    ("Entertainment: Books", "easy", "Who wrote Pride and Prejudice?", "Jane Austen", ["Charlotte Bronte", "Emily Bronte", "Mary Shelley"]),
    ("Entertainment: Books", "medium", "Who wrote Don Quixote?", "Miguel de Cervantes", ["Lope de Vega", "Gabriel Garcia Marquez", "Federico Garcia Lorca"]),
    ("Entertainment: Books", "easy", "Who wrote Frankenstein?", "Mary Shelley", ["Bram Stoker", "Edgar Allan Poe", "Percy Bysshe Shelley"]),
    ("Entertainment: Books", "medium", "Who wrote Crime and Punishment?", "Fyodor Dostoevsky", ["Leo Tolstoy", "Anton Chekhov", "Ivan Turgenev"]),
    ("Entertainment: Books", "medium", "Who wrote One Hundred Years of Solitude?", "Gabriel Garcia Marquez", ["Isabel Allende", "Jorge Luis Borges", "Pablo Neruda"]),
    ("Entertainment: Books", "medium", "Who wrote Things Fall Apart?", "Chinua Achebe", ["Wole Soyinka", "Ngugi wa Thiong'o", "Ben Okri"]),
    ("Entertainment: Books", "hard", "The Tale of Genji, often called the world's first novel, was written by whom?", "Murasaki Shikibu", ["Sei Shonagon", "Lady Nijō", "Basho"]),
    ("Entertainment: Books", "medium", "Who wrote Their Eyes Were Watching God?", "Zora Neale Hurston", ["Toni Morrison", "Nella Larsen", "Alice Walker"]),
    ("Entertainment: Books", "medium", "Who wrote Invisible Man, the 1952 novel about a Black man in America?", "Ralph Ellison", ["Richard Wright", "James Baldwin", "H. G. Wells"]),
    ("Entertainment: Books", "medium", "Who wrote Beloved?", "Toni Morrison", ["Maya Angelou", "Octavia Butler", "Alice Walker"]),
    ("Entertainment: Books", "hard", "Who wrote Kindred?", "Octavia E. Butler", ["Ursula K. Le Guin", "N. K. Jemisin", "Samuel R. Delany"]),
    ("Entertainment: Books", "medium", "Who wrote The Left Hand of Darkness?", "Ursula K. Le Guin", ["Margaret Atwood", "Philip K. Dick", "Arthur C. Clarke"]),
    ("Entertainment: Books", "hard", "Who wrote Neuromancer?", "William Gibson", ["Neal Stephenson", "Isaac Asimov", "Philip K. Dick"]),
    ("Entertainment: Music", "easy", "Beethoven's Ninth Symphony ends with a setting of which poem?", "Ode to Joy", ["Ode to a Nightingale", "The Raven", "If—"]),
    ("Entertainment: Music", "easy", "Who composed The Four Seasons?", "Antonio Vivaldi", ["Johann Sebastian Bach", "George Frideric Handel", "Joseph Haydn"]),
    ("Entertainment: Music", "medium", "The Rite of Spring, which caused a famous stir at its 1913 premiere, was composed by whom?", "Igor Stravinsky", ["Claude Debussy", "Sergei Rachmaninoff", "Bela Bartok"]),
    ("Entertainment: Music", "medium", "Miles Davis's album Kind of Blue was released in what year?", "1959", ["1949", "1969", "1975"]),
    ("Entertainment: Music", "medium", "Who composed Rhapsody in Blue?", "George Gershwin", ["Aaron Copland", "Duke Ellington", "Leonard Bernstein"]),
    ("Entertainment: Music", "easy", "Who composed Swan Lake?", "Pyotr Ilyich Tchaikovsky", ["Igor Stravinsky", "Sergei Prokofiev", "Johann Strauss II"]),
    ("Entertainment: Music", "medium", "Who composed the opera Carmen?", "Georges Bizet", ["Giuseppe Verdi", "Giacomo Puccini", "Richard Wagner"]),
    ("Entertainment: Music", "medium", "Fela Kuti is the central figure of which musical style?", "Afrobeat", ["Reggae", "Bossa nova", "Highlife"]),
    ("Entertainment: Music", "medium", "Ravi Shankar was a master of which instrument?", "Sitar", ["Tabla", "Oud", "Koto"]),
    ("Entertainment: Music", "easy", "Bob Dylan was awarded the Nobel Prize in Literature in what year?", "2016", ["2006", "1996", "2020"]),
    ("Entertainment: Film", "medium", "Who directed Citizen Kane?", "Orson Welles", ["Alfred Hitchcock", "John Ford", "Frank Capra"]),
    ("Entertainment: Film", "medium", "Who directed Seven Samurai?", "Akira Kurosawa", ["Yasujiro Ozu", "Kenji Mizoguchi", "Hayao Miyazaki"]),
    ("Entertainment: Film", "easy", "Who directed Spirited Away?", "Hayao Miyazaki", ["Isao Takahata", "Satoshi Kon", "Makoto Shinkai"]),
    ("Entertainment: Film", "medium", "Who directed 2001: A Space Odyssey?", "Stanley Kubrick", ["Ridley Scott", "Andrei Tarkovsky", "Steven Spielberg"]),
    ("Entertainment: Film", "medium", "Who directed Psycho?", "Alfred Hitchcock", ["Orson Welles", "Billy Wilder", "Fritz Lang"]),
    ("Entertainment: Film", "medium", "Who directed Do the Right Thing?", "Spike Lee", ["John Singleton", "Jordan Peele", "Ava DuVernay"]),
    ("Entertainment: Film", "easy", "Parasite, the first non-English-language film to win the Oscar for Best Picture, was directed by whom?", "Bong Joon-ho", ["Park Chan-wook", "Hirokazu Kore-eda", "Ang Lee"]),
    ("Entertainment: Film", "medium", "Metropolis, the 1927 science-fiction film, was directed by whom?", "Fritz Lang", ["F. W. Murnau", "Charlie Chaplin", "Georges Melies"]),
    ("Entertainment: Film", "medium", "Who directed The Godfather?", "Francis Ford Coppola", ["Martin Scorsese", "Brian De Palma", "Sergio Leone"]),
    ("Sports", "easy", "The first modern Olympic Games were held in what year?", "1896", ["1900", "1892", "1912"]),
    ("Sports", "medium", "The official marathon distance is how long?", "42.195 kilometers", ["40 kilometers", "26 miles exactly", "50 kilometers"]),
    ("Sports", "easy", "Who invented basketball?", "James Naismith", ["Abner Doubleday", "Walter Camp", "William G. Morgan"]),
    ("Sports", "medium", "The first FIFA World Cup was held in what year?", "1930", ["1924", "1950", "1934"]),
    ("Sports", "easy", "Which country has won the men's FIFA World Cup the most times?", "Brazil", ["Germany", "Italy", "Argentina"]),
    ("Sports", "medium", "Which Grand Slam tennis tournament is played on grass?", "Wimbledon", ["The French Open", "The US Open", "The Australian Open"]),
    ("Sports", "medium", "Jesse Owens won four gold medals at which Olympic Games?", "Berlin 1936", ["London 1948", "Los Angeles 1932", "Paris 1924"]),
    ("Sports", "medium", "Jackie Robinson broke the color line in modern Major League Baseball in what year?", "1947", ["1945", "1955", "1961"]),
    ("Sports", "medium", "Nadia Comaneci scored the first perfect 10 in Olympic gymnastics at which Games?", "Montreal 1976", ["Munich 1972", "Moscow 1980", "Los Angeles 1984"]),
    ("Sports", "medium", "Usain Bolt's world record in the 100 meters is what time?", "9.58 seconds", ["9.69 seconds", "9.95 seconds", "8.99 seconds"]),
    ("Sports", "medium", "The first Tour de France was held in what year?", "1903", ["1896", "1923", "1886"]),
    ("Sports", "medium", "The first FIFA Women's World Cup was held in what year?", "1991", ["1971", "1999", "1985"]),
    ("Politics", "easy", "How many voting members sit in the United States House of Representatives?", "435", ["100", "538", "400"]),
    ("Politics", "easy", "How many United States senators are there?", "100", ["50", "435", "200"]),
    ("Politics", "easy", "How many amendments does the United States Constitution currently have?", "27", ["10", "21", "33"]),
    ("Politics", "medium", "The 19th Amendment, guaranteeing women the vote in the United States, was ratified in what year?", "1920", ["1868", "1965", "1848"]),
    ("Politics", "medium", "The 26th Amendment lowered the US voting age to 18 in what year?", "1971", ["1964", "1945", "1982"]),
    ("Politics", "medium", "The United Nations was founded in what year?", "1945", ["1919", "1948", "1955"]),
    ("Politics", "medium", "NATO was founded in what year?", "1949", ["1945", "1955", "1939"]),
    ("Politics", "medium", "The Universal Declaration of Human Rights was adopted in what year?", "1948", ["1945", "1776", "1966"]),
    ("Vehicles", "easy", "The Wright brothers' first powered flight was in what year?", "1903", ["1896", "1914", "1886"]),
    ("Vehicles", "medium", "Karl Benz is credited with building the first practical automobile, the Patent-Motorwagen, in what year?", "1886", ["1908", "1876", "1895"]),
    ("Vehicles", "easy", "The Ford Model T was introduced in what year?", "1908", ["1903", "1920", "1896"]),
    ("Vehicles", "medium", "Chuck Yeager was the first pilot to do what in level flight?", "Fly faster than sound", ["Fly across the Atlantic", "Orbit the Earth", "Land on an aircraft carrier"]),
    ("Vehicles", "medium", "The rocket that launched the Apollo missions to the Moon was called what?", "Saturn V", ["Atlas V", "Falcon Heavy", "Soyuz"]),
    ("Vehicles", "medium", "Commercial flights of the Concorde supersonic airliner ended in what year?", "2003", ["1991", "2012", "1976"]),
    ("General Knowledge", "easy", "The primary colors of light are red, green, and what?", "Blue", ["Yellow", "White", "Orange"]),
    ("General Knowledge", "medium", "Which of these years was a leap year?", "2000", ["1900", "1800", "2100"]),
    ("General Knowledge", "easy", "The Nobel Prizes were first awarded in what year?", "1901", ["1895", "1918", "1880"]),
    ("General Knowledge", "medium", "Louis Braille developed his reading system in which country?", "France", ["Germany", "England", "United States"]),
    ("General Knowledge", "medium", "Esperanto was created by whom?", "L. L. Zamenhof", ["Noah Webster", "Ludwig Wittgenstein", "Eliezer Ben-Yehuda"]),
    ("General Knowledge", "medium", "The game that developed into modern chess began in which country?", "India", ["China", "Persia", "Italy"]),
    ("General Knowledge", "medium", "Who proposed the World Wide Web in 1989 while working at CERN?", "Tim Berners-Lee", ["Vint Cerf", "Alan Turing", "Grace Hopper"]),
    ("General Knowledge", "medium", "Grace Hopper is celebrated in computing for leading work on what?", "The first compiler", ["The computer mouse", "The World Wide Web", "The transistor"]),
    ("Science: Computers", "medium", "ARPANET, a forerunner of the internet, sent its first messages in what year?", "1969", ["1959", "1983", "1976"]),
    ("Science: Computers", "medium", "Alan Turing described the imitation game, now called the Turing test, in what year?", "1950", ["1936", "1960", "1943"]),
]


def load_questions():
    with open(DATABASE_FILE, encoding="utf-8") as file:
        return json.load(file)


def save_questions(questions):
    temporary = DATABASE_FILE + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(questions, file, indent=2, ensure_ascii=False)
        file.write("\n")
    os.replace(temporary, DATABASE_FILE)


def check_new_questions():
    seen = set()
    for category, difficulty, question, correct, wrong in QUESTIONS:
        if difficulty not in ("easy", "medium", "hard"):
            raise SystemExit(f"Bad difficulty: {question}")
        if not question.endswith("?"):
            raise SystemExit(f"Question should end with a question mark: {question}")
        answers = [correct, *wrong]
        if len(wrong) != 3 or len(set(answers)) != 4:
            raise SystemExit(f"Need four different answers: {question}")
        if question in seen:
            raise SystemExit(f"Repeated new question: {question}")
        seen.add(question)


def main():
    check_new_questions()
    questions = load_questions()
    removed_facts = 0
    for item in questions:
        if "fact" in item or "fact_source" in item:
            item.pop("fact", None)
            item.pop("fact_source", None)
            removed_facts += 1

    seen = {item["question"] for item in questions}
    added = 0
    for category, difficulty, question, correct, wrong in QUESTIONS:
        if question in seen:
            continue
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

    save_questions(questions)
    print(f"Removed fact fields from {removed_facts} questions.")
    print(f"Added {added} new questions.")
    print(f"The database now has {len(questions)} questions.")


if __name__ == "__main__":
    main()
