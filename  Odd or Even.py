# Odd or Even?

# Function to check if a number is odd or even
#Define a function called check_odd_or_even that is a number
def check_odd_or_even(number):
    # The expression 'number % 2 == 0' is like saying, 
    # The number you enter is divisible by 2 and doesn't have a remainder.
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Get user input
# This line of code is asking the user to enter an integer, 
# and the entered value is stored in the variable user_input as a string.
user_input = input("Enter an integer: ")

# Validate user input
try:
    user_number = int(user_input)
    result = check_odd_or_even(user_number)
    print(f"The number {user_number} is {result}.")
except ValueError:
    print("Invalid input. Please enter a valid integer.")