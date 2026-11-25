"""Calculate and classify BMI from weight in kilograms and height in metres."""

import math


def read_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if math.isfinite(value) and value > 0:
                return value
        except ValueError:
            pass
        print("Enter a finite number greater than zero, such as 70 or 1.75.")


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def main():
    print("BMI Calculator")
    try:
        while True:
            weight = read_positive_number("Weight (kg): ")
            height = read_positive_number("Height (m): ")
            bmi = weight / height / height
            if math.isfinite(bmi) and bmi > 0:
                print(f"BMI: {bmi:.2f}\nCategory: {classify_bmi(bmi)}")
                return
            print("Those measurements produce a BMI outside the supported number range. Try again.")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting BMI Calculator.")


if __name__ == "__main__":
    main()
