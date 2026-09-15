numbers = []

while True:
    num1 = int(input("enter num 1: "))
    num2 = int(input("enter num 2: "))
    numbers.append((num1, num2))
    print(numbers)
    user_choice = input ("add another y/n: ").lower()
    if user_choice == "y":
        continue
    elif user_choice == "n":
        break

