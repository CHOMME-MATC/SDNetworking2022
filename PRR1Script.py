'''
Date: 1/24/22
Author: Chance Homme

This script is responsible for taking a users name and age and storing it as a vairable,
then printing a statement with a modified variable which will personally address the user and state the users age in five years.

The firstName variable is responsible for taking the users name.
The age variable is responsible for taking the users age.
the agePlus5 variable is responsible for adding 5 to the integer value of the age variable.

'''

firstName = input("Enter your first name:")

age = input("Enter your age:")

agePlus5 = int(age) + 5

print("Hello", firstName.capitalize() + ".", "In five years, you will be", str(agePlus5) + "!")
