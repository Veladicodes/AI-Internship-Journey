import random

target = random.randint(1, 100)
print("Guess a number between 1 and 100")

while True:
    guess = int(input("Enter your guess: "))
    if guess < target:
        print("Too low!")
    elif guess > target:
        print("Too high!")
    else:
        print("Correct!")
        break
