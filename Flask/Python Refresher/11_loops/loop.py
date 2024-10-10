number = 6
player = input("Would you like to play? (Y/n) ")

while player != "n":
    guess = int(input("Pick a number between 1 and 10: "))
    if guess == number:
        print("You guessed correctly dude!")
    elif abs(number - guess) == 1:
        print("You were off by 1.")
    elif abs(number - guess) == 2:
        print("You were off by 2.")
    else:
        print("Sorry, it's wrong!")

    player = input("Would you like to play again? (Y/n) ")
      