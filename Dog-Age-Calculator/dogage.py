def calculate_dog_age(human_age):
    if human_age < 0:
        return None
    if human_age <= 2:
        return human_age * 10.5
    return 21 + (human_age - 2) * 4


human_age = int(input("Enter a dog's age in human years: "))
dog_age = calculate_dog_age(human_age)

if dog_age is None:
    print("Age must be a positive number.")
else:
    print(f"The dog's age in dog years is {dog_age}.")