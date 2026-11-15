"""Add original sports, music, and movie-and-TV questions."""

import json

DATABASE_FILE = "questions.json"

# category, difficulty, question, correct answer, three wrong answers
QUESTIONS = [
    ("Sports", "easy", "How many players from one team are on the court in a standard basketball game?", "5", ["6", "7", "11"]),
    ("Sports", "easy", "How many players from one team are on the field in baseball?", "9", ["8", "10", "11"]),
    ("Sports", "easy", "How many innings are in a standard baseball game?", "9", ["7", "8", "10"]),
    ("Sports", "easy", "How many periods are in a standard National Hockey League game?", "3", ["2", "4", "5"]),
    ("Sports", "easy", "A standard soccer match lasts how many minutes, before added stoppage time?", "90", ["60", "80", "120"]),
    ("Sports", "easy", "Which country has won the most FIFA men's World Cups?", "Brazil", ["Germany", "Italy", "Argentina"]),
    ("Sports", "medium", "Which country won the 2022 FIFA men's World Cup?", "Argentina", ["France", "Brazil", "Croatia"]),
    ("Sports", "easy", "The Super Bowl decides the champion of which league?", "The NFL", ["The NBA", "The NHL", "Major League Baseball"]),
    ("Sports", "easy", "The Stanley Cup is the championship trophy of which sport?", "Ice hockey", ["Basketball", "Baseball", "Lacrosse"]),
    ("Sports", "easy", "The World Series decides the champion of which sport?", "Baseball", ["Basketball", "American football", "Ice hockey"]),
    ("Sports", "easy", "Wimbledon tennis is played on which surface?", "Grass", ["Clay", "Hard court", "Carpet"]),
    ("Sports", "medium", "The Masters golf tournament is played at which course?", "Augusta National", ["St Andrews", "Pebble Beach", "Pinehurst"]),
    ("Sports", "easy", "How many holes are in a standard round of golf?", "18", ["9", "12", "21"]),
    ("Sports", "easy", "A marathon is about how many miles?", "26.2", ["13.1", "20", "30"]),
    ("Sports", "easy", "How many interlocking rings are on the Olympic flag?", "5", ["4", "6", "7"]),
    ("Sports", "easy", "Which city hosted the 2024 Summer Olympics?", "Paris", ["London", "Tokyo", "Los Angeles"]),
    ("Sports", "medium", "Which country hosted the 2016 Summer Olympics?", "Brazil", ["China", "Japan", "United Kingdom"]),
    ("Sports", "easy", "The Tour de France is a race in which sport?", "Cycling", ["Running", "Auto racing", "Skiing"]),
    ("Sports", "medium", "In the Tour de France, the yellow jersey is worn by whom?", "The overall race leader", ["The best sprinter", "The best climber", "The youngest rider"]),
    ("Sports", "easy", "In baseball, how many strikes make a strikeout?", "3", ["2", "4", "5"]),
    ("Sports", "easy", "How many pins are set up in a standard game of ten-pin bowling?", "10", ["8", "9", "12"]),
    ("Sports", "easy", "Which of these sports is played with a puck?", "Ice hockey", ["Soccer", "Lacrosse", "Field hockey"]),
    ("Sports", "easy", "Serena Williams is famous for which sport?", "Tennis", ["Golf", "Basketball", "Track and field"]),
    ("Sports", "easy", "Michael Jordan is most famous for which sport?", "Basketball", ["Baseball", "American football", "Boxing"]),
    ("Sports", "easy", "Muhammad Ali is famous for which sport?", "Boxing", ["Wrestling", "Fencing", "Judo"]),
    ("Sports", "medium", "The Ashes is a famous contest in which sport?", "Cricket", ["Rugby", "Polo", "Rowing"]),
    ("Sports", "easy", "How many players are on a cricket team?", "11", ["9", "13", "15"]),
    ("Sports", "easy", "In soccer, a hat-trick is how many goals by one player in a match?", "3", ["2", "4", "5"]),
    ("Sports", "easy", "The Indianapolis 500 is which kind of race?", "An automobile race", ["A horse race", "A boat race", "A bicycle race"]),
    ("Sports", "medium", "A men's singles final at a tennis Grand Slam is the best of how many sets?", "5", ["3", "4", "7"]),
    ("Sports", "easy", "Simone Biles is famous for which sport?", "Gymnastics", ["Figure skating", "Diving", "Track and field"]),
    ("Sports", "easy", "The Kentucky Derby is a race for which animals?", "Horses", ["Dogs", "Cars", "Cyclists"]),
    ("Sports", "easy", "In American football, a touchdown is worth how many points before the extra kick?", "6", ["3", "7", "2"]),
    ("Sports", "easy", "In American football, a field goal is worth how many points?", "3", ["1", "2", "6"]),
    ("Sports", "easy", "Which NBA team plays its home games in Boston?", "The Boston Celtics", ["The Boston Bruins", "The New England Patriots", "The Boston Red Sox"]),
    ("Sports", "easy", "Usain Bolt is famous for which kind of race?", "Sprinting", ["The marathon", "The hurdles only", "Race walking"]),
    ("Sports", "easy", "How many skaters from one team, including the goalie, are on the ice in hockey?", "6", ["5", "7", "11"]),
    ("Sports", "easy", "The Ryder Cup is a team event in which sport?", "Golf", ["Tennis", "Polo", "Sailing"]),
    ("Sports", "medium", "In baseball, a perfect game means the pitcher did what?", "Did not let anyone reach base", ["Struck out every batter", "Allowed no runs but some hits", "Threw only strikes"]),
    ("Music", "easy", "The Beatles were from which city?", "Liverpool", ["London", "Manchester", "Birmingham"]),
    ("Music", "easy", "How many members were in the Beatles?", "4", ["3", "5", "6"]),
    ("Music", "easy", "Freddie Mercury was the lead singer of which band?", "Queen", ["The Who", "Led Zeppelin", "The Rolling Stones"]),
    ("Music", "easy", "Which band recorded Bohemian Rhapsody?", "Queen", ["The Beatles", "Pink Floyd", "ABBA"]),
    ("Music", "medium", "Beethoven's symphony that includes the Ode to Joy is which number?", "The 9th", ["The 5th", "The 3rd", "The 7th"]),
    ("Music", "easy", "Aretha Franklin is known by which nickname?", "The Queen of Soul", ["The Queen of Pop", "The Empress of Jazz", "The First Lady of Song"]),
    ("Music", "easy", "Elvis Presley was born in which U.S. state?", "Mississippi", ["Tennessee", "Texas", "Alabama"]),
    ("Music", "easy", "The Grammy Awards honor achievements in what?", "Music", ["Film", "Television", "Theater"]),
    ("Music", "easy", "A violin is usually played with what?", "A bow", ["A pick", "Mallets", "The feet"]),
    ("Music", "easy", "Which woodwind instrument is held sideways when it is played?", "The flute", ["The clarinet", "The oboe", "The bassoon"]),
    ("Music", "medium", "The saxophone is named after which inventor?", "Adolphe Sax", ["Antonio Stradivari", "Bartolomeo Cristofori", "John Philip Sousa"]),
    ("Music", "easy", "Who released the album Thriller?", "Michael Jackson", ["Prince", "Stevie Wonder", "Whitney Houston"]),
    ("Music", "easy", "Michael Jackson is often called what?", "The King of Pop", ["The King of Rock and Roll", "The King of Soul", "The King of Reggae"]),
    ("Music", "easy", "Elvis Presley is often called what?", "The King of Rock and Roll", ["The King of Pop", "The King of Soul", "The King of Country"]),
    ("Music", "easy", "Beyonce was a member of which group before her solo career?", "Destiny's Child", ["TLC", "The Supremes", "Spice Girls"]),
    ("Music", "medium", "Who composed The Four Seasons?", "Antonio Vivaldi", ["Johann Sebastian Bach", "George Frideric Handel", "Joseph Haydn"]),
    ("Music", "easy", "The trumpet belongs to which instrument family?", "Brass", ["Strings", "Woodwinds", "Percussion"]),
    ("Music", "easy", "The violin belongs to which instrument family?", "Strings", ["Brass", "Woodwinds", "Percussion"]),
    ("Music", "easy", "Bob Marley is most associated with which style of music?", "Reggae", ["Salsa", "Blues", "Opera"]),
    ("Music", "medium", "Hip-hop culture began in which New York borough?", "The Bronx", ["Brooklyn", "Queens", "Manhattan"]),
    ("Music", "medium", "Who composed the opera The Magic Flute?", "Wolfgang Amadeus Mozart", ["Ludwig van Beethoven", "Giuseppe Verdi", "Richard Wagner"]),
    ("Music", "easy", "Adele released the song Rolling in the Deep on which album?", "21", ["19", "25", "30"]),
    ("Music", "easy", "Taylor Swift's first albums were mainly which genre?", "Country", ["Opera", "Jazz", "Reggae"]),
    ("Music", "easy", "How many lines are on a standard music staff?", "5", ["4", "6", "8"]),
    ("Music", "medium", "In 4/4 time, a note that fills a whole measure by itself is called a what?", "A whole note", ["A half note", "A quarter note", "An eighth note"]),
    ("Music", "easy", "The 1969 music festival held in Bethel, New York, is known as what?", "Woodstock", ["Monterey Pop", "Live Aid", "Lollapalooza"]),
    ("Music", "easy", "Louis Armstrong is most associated with which instrument?", "The trumpet", ["The saxophone", "The piano", "The trombone"]),
    ("Music", "easy", "Yo-Yo Ma is famous for playing which instrument?", "The cello", ["The violin", "The harp", "The flute"]),
    ("Music", "easy", "Which famous composer continued to write music after he lost his hearing?", "Ludwig van Beethoven", ["Johann Sebastian Bach", "Wolfgang Amadeus Mozart", "Franz Schubert"]),
    ("Music", "easy", "A cappella singing is performed how?", "Without instruments", ["With a full orchestra", "Only with drums", "Only through a microphone"]),
    ("Music", "easy", "Flamenco music and dance began in which country?", "Spain", ["Portugal", "Italy", "Argentina"]),
    ("Music", "medium", "The didgeridoo is a traditional instrument of which people?", "Aboriginal Australians", ["The Maori", "The Inuit", "The Zulu"]),
]


def main():
    with open(DATABASE_FILE, encoding="utf-8") as handle:
        questions = json.load(handle)
    with open("extra_questions.json", encoding="utf-8") as handle:
        extras = json.load(handle)

    seen = {item["question"] for item in questions}
    added = 0

    def add(category, difficulty, question, correct, wrong):
        nonlocal added
        if question in seen:
            return
        if len({correct, *wrong}) != 4:
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

    for category, difficulty, question, correct, wrong in QUESTIONS:
        add(category, difficulty, question, correct, wrong)
    for item in extras:
        add(item["category"], item["difficulty"], item["question"], item["correct_answer"], item["incorrect_answers"])

    with open(DATABASE_FILE, "w", encoding="utf-8") as handle:
        json.dump(questions, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Added {added} questions.")
    print(f"The database now has {len(questions)} questions.")


if __name__ == "__main__":
    main()
