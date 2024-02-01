import json
import random
import tkinter as tk

#file path
file_path = r'C:\Users\ikemo\PythonProjects\Hangman\wordsapi_sample.json'

def get_random_entry_with_details(json_data):
    while True:
        try:
            # Get a random key from the dictionary
            random_key = random.choice(list(json_data.keys()))

            # Extract details for the randomly selected key
            random_entry = json_data.get(random_key, {})
            definitions = random_entry.get("definitions", [])

            # Extract specific information from definitions
            selected_definition = None
            for definition in definitions:
                if 'not alike or similar' in definition.get('definition', ''):
                    selected_definition = {
                        'definition': definition.get('definition', ''),
                        'synonyms': definition.get('synonyms', []),
                    }
                    break

            # If the selected definition is found, return the details
            if selected_definition is not None:
                return {
                    "Random Key": random_key,
                    "Selected Definition": selected_definition,
                    "Letters": random_entry.get("letters", 0)
                }

        except Exception as e:
            # Handle any exceptions that might occur during the process
            print(f"Error: {e}")

hangman_art = [
    "   +---+\n   |   |\n       |\n       |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n       |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n   |   |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|   |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n  /    |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n  / \\  |\n       |\n========="
]

def wrong_hangman(mistake):
    hangman_label.config(text=hangman_art[mistake])

def check_guess(guess):
    global word_blanks
    guess = guess.lower()
    if guess in random_entry_details.get("Random Key"):
        for i in range(random_entry_details.get("Letters", 0)):
            if random_entry_details.get("Random Key")[i] == guess:
                word_blanks = word_blanks[:i] + guess + word_blanks[i+1:]
        word_label.config(text=word_blanks)
        if '_' not in word_blanks:
                end_game("You win")
    else:
        global mistake
        mistake +=1
        wrong_hangman(mistake)
        if mistake == 6:
            end_game("You lose")

def end_game(result):
    if result == "You win":
        result_text="You win!"
    else:
        result_text = "You lose, the correct answer is " + random_entry_details.get("Random Key")
        result_label.config(text = result_text)
        guess_letter.config(state = "disabled")
        guess_button.config(state = "disabled")

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        oxford_Dictionary = json.load(file)

        # Call the function in a loop until a non-None definition is found
        random_entry_details = get_random_entry_with_details(oxford_Dictionary)
        # Print the details
        for key, value in random_entry_details.items():
            print(f"{key}: {value}")

        #print("ikem this is it: " * random_entry_details.get("Letters", 0))


        root = tk.Tk()
        root.title("Hangman")

        hangman_label = tk.Label(root, font=("CourierK", 16))
        hangman_label.grid(row=0, column=0)

        word_blanks = '_' * random_entry_details.get("Letters", 0)
        #print(random_entry_details.get("Letters", 0))
        word_label = tk.Label(root, text=word_blanks, font=("Arial", 24))
        word_label.grid(row=1, column=0)

        guess_letter = tk.Entry(root, width=3, font=("Arial", 24))
        guess_letter.grid(row=2, column=0)
        guess_button = tk.Button(root, text="Guess", command=lambda: check_guess(guess_letter.get()))
        guess_button.grid(row=2, column=1)

        result_label = tk.Label(root, font=("Arial", 24))
        result_label.grid(row=3, column=0)


        mistake = 0
        wrong_hangman(mistake)

        root.mainloop()

except FileNotFoundError:
    print(f"File not found: {file_path}")
except json.JSONDecodeError:
    print(f"Error decoding JSON in file: {file_path}")
except UnicodeDecodeError:
    print(f"Error decoding file with UTF-8 encoding: {file_path}")