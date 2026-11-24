
import random
words = [
    "python",
    "hangman",
    "computer",
    "developer",
    "programming",
    "galaxy",
    "science"
]
print("Word list created successfully!")
print("Total words:", len(words))
print("Available words:", words)
secret_word = random.choice(words).lower()
correct_guesses = set()
wrong_guesses = set()

max_mistakes = 6
mistakes = 0


stages = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]

def display_word():
    masked_word = ""

    for letter in secret_word:
        if letter in correct_guesses:
            masked_word += letter.upper() + " "
        else:
            masked_word += "_ "

    return masked_word



print("===== WELCOME TO HANGMAN GAME =====")

while mistakes < max_mistakes and not all(
    letter in correct_guesses for letter in secret_word
):

    print(stages[mistakes])
    print("Word:", display_word())
    print("Wrong guesses:", ", ".join(sorted(wrong_guesses)))
    print("Remaining attempts:", max_mistakes - mistakes)

    guess = input("Guess a letter: ").lower().strip()

  
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter only one alphabet letter!\n")
        continue

  
    if guess in correct_guesses or guess in wrong_guesses:
        print("You already guessed that letter!\n")
        continue

  
    if guess in secret_word:
        correct_guesses.add(guess)
        print("Correct guess!\n")
    else:
        wrong_guesses.add(guess)
        mistakes += 1
        print("Wrong guess!\n")



print(stages[mistakes])

if all(letter in correct_guesses for letter in secret_word):
    print("Congratulations! You won!")
    print("The secret word was:", secret_word.upper())
else:
    print("Game Over! You lost.")
    print("The secret word was:", secret_word.upper())
