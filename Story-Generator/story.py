import random
when = [
    "A few years ago",
    "Yesterday",
    "Last night",
    "A long time ago",
    "On 20th January"
]
who = [
    "a rabbit",
    "an elephant",
    "a mouse",
    "a turtle",
    "a cat"
]
names = [
    "Ali",
    "Miriam",
    "Daniel",
    "Houuk",
    "Starwalker"
]
places = [
    "Barcelona",
    "India",
    "Germany",
    "Venice",
    "England"
]
went_to = [
    "cinema",
    "university",
    "seminar",
    "school",
    "laundry"
]
happened = [
    "made a lot of friends",
    "ate a burger",
    "found a secret key",
    "solved a mystery",
    "wrote a book"
]
story = (
    f"{random.choice(when)}, "
    f"{random.choice(names)} the {random.choice(who)} "
    f"from {random.choice(places)} went to the "
    f"{random.choice(went_to)} and "
    f"{random.choice(happened)}."
)
print(story)