"""Generate passwords with user-selected character types."""

import secrets
import string


MIN_LENGTH = 8
CHARACTER_TYPES = {
    "Uppercase letters": string.ascii_uppercase,
    "Lowercase letters": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation,
}


def ask_yes_no(prompt):
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in {"y", "yes", "n", "no"}:
            return answer in {"y", "yes"}
        print("Enter y for yes or n for no.")


def read_length():
    while True:
        try:
            length = int(input(f"Password length (at least {MIN_LENGTH}): "))
            if length >= MIN_LENGTH:
                return length
        except ValueError:
            pass
        print(f"Enter a whole number of {MIN_LENGTH} or greater.")


def generate_password(length, selected_types):
    pool = "".join(selected_types)
    characters = [secrets.choice(characters) for characters in selected_types]
    characters.extend(secrets.choice(pool) for _ in range(length - len(characters)))
    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)


def main():
    print("Random Password Generator")
    try:
        while True:
            length = read_length()
            while True:
                selected_types = [
                    characters
                    for name, characters in CHARACTER_TYPES.items()
                    if ask_yes_no(f"Include {name.lower()}?")
                ]
                if len(selected_types) >= 2:
                    break
                print("Select at least two character types.")

            print(f"\nGenerated password: {generate_password(length, selected_types)}")
            if not ask_yes_no("Generate another password?"):
                return
    except (EOFError, KeyboardInterrupt):
        print("\nExiting Random Password Generator.")


if __name__ == "__main__":
    main()
