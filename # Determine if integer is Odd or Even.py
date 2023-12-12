# Determine if integer is Odd or Even 
# Get user input
user_input = input("Enter an integer: ")

# Check if the input is a valid integer
try:
    number = int(user_input)
except ValueError:
    print("Invalid input. Please enter a valid integer.")
    exit()
# Check if the number is odd or even
if number % 2 == 0:
    print(f"{number} is even.")
else:
    print(f"{number} is odd.")