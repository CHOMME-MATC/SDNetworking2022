'''
Date: 1/24/22
Author: Chance Homme

This script is responsible for creating a variable which contains a users first and last name, then
checking the input for two alphanumeric names and using them in a response print statement.
If the script finds there is not two names or that the names are not alphanumeric, an error will occur
telling the user how to correctly input their response.

'''

#====================================================================================================
#firstLast is the variable which will collect the first and last name of the user.
#answerList is the variable which will itemize the response into a list.
#count is the variable which will serve as a check for alphanumeric characters in the user response.
#====================================================================================================

firstLast = input("Enter your full name without your middle initail:")

answerList = list(firstLast.split())

count = 0

#=================================================================================================
#The for loop will check for alphanumeric characters in all of the items in answerList, if the 
#items in answerList are alpha characters only, the count will be incremented by one. Once the for
#loop has iterated through the list, the if statement will check the count for only 2 names (items)
#in the answerList and if there is just 2 and only 2 names in the answerList, it will print the
#response statement, otherwise, it will print an error response.
#=================================================================================================

for items in answerList:
    items.isalpha()
    if items.isalpha() == True:
            count +=1
            
if count == 2 and len(answerList) == 2:
    print("Welcome to Python", answerList[0].capitalize() + ".", answerList[1].capitalize(), "is a really interesting surname! Are you related to the famous Victoria", answerList[1].capitalize() + "?")    

else:
    print("Error: Only type your first and last name in alphanumeric characters when prompted.")
