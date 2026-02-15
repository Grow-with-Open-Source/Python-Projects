# Temperature Converter
# Converts temperature between Celsius, Fahrenheit, and Kelvin

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32

choice_Action = {
    1: ("Celsius to Fahrenheit", celsius_to_fahrenheit),
    2: ("Fahrenheit to Celsius", fahrenheit_to_celsius),
    3: ("Celsius to Kelvin", celsius_to_kelvin),
    4: ("Kelvin to Celsius", kelvin_to_celsius),
    5: ("Fahrenheit to Kelvin", fahrenheit_to_kelvin),
    6: ("Kelvin to Fahrenheit", kelvin_to_fahrenheit)

}

def main():
    print("🌡️ Temperature Converter")
    for option in choice_Action.items(): print(f"{option[0]}. {option[1][0]}") # print number with option

    while True:

        while True:
            try:
                choice = int(input("Enter choice (1–6) or -1 for exit: "))
            except ValueError:
                print("You can not input strings")
            else: break

        if choice == -1: break
        elif choice in choice_Action:
            parameter1, parameter2 = choice_Action[choice][0].split(" to ")

            while True:
                try:
                    value = float(input(f"Enter: {parameter1} "))
                except ValueError:
                    print("You can not input strings")
                else: break

            print(f"{value} {parameter1} = {choice_Action[choice][1](value):.2f} {parameter2}")
        else:
            print(f"{choice} is invalid, please enter values from 1 - 6")
            continue

if __name__ == "__main__":
    main()
