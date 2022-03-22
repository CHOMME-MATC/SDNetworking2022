'''
Author: Chance Homme
Date: 2/9/22

This script is responsible for creating get request through API's using the 'requests' library and exploring the output as well as entering
parameters to change the response of the api call. This code also creates a function based card game using the "deckofcardsapi" api.

'''



#Original code from postman

import requests  # The import function is calling to import the 'requests' library which is needed to opperate http requests 

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"    # url is specifiying the api url we would like to make requests from

payload={} # payload is an empty dictionary used in the data parameter
headers = {} # headers is an empty dictionary used in the headers parameter

response = requests.request("GET", url, headers=headers, data=payload) # response is a variable that is calling a http get request using the 
                                                                       # request library with the url variable as the destination url, and the
                                                                       # headers and payload dictionaries as the headers and data parameters
print(response.text)




# Modified version for questions 2-3. This code is the same function in principal except the variable has been changed from url to Myurl in all
# fields where it has been called


import requests

Myurl = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

payload={}
headers = {}

response = requests.request("GET", Myurl, headers=headers, data=payload)

print(response.text)



#Question 4


import requests 

Myurl = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" 
payload={}
headers = {}


response = requests.request("GET", Myurl, headers=headers, data=payload) 

#The above code is the same as the past iterations

deck = response.json() # deck is a variable which contains the json response of the response variable in a dictionary

deck_id = deck['deck_id'] # the deck_id variable contains the value of the deck_id key in the deck dictionary


print('Your deck is shuffled and ready. Your deck id is:', deck_id) # Instead of printing the entire response of the response variable,
                                                                    # the print statement is now picking a value out of the dictionary
                                                                    # containing the json response





# Question 5-7



import requests # The import function is calling to import the 'requests' library which is needed to opperate http requests  

url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"  # url is specifiying the api url we would like to make requests from
  

payload={} 
headers = {} 

response = requests.request("GET", url, headers=headers, data=payload) # response is a variable that is calling a http get request using the 
                                                                       # request library with the url variable as the destination url, and the
                                                                       # headers and payload dictionaries as the headers and data parameters

card_count = input('Your deck has been shuffled, how many cards would you like to draw? ') # card_count is asking for user input on the ammount
                                                                                           # of cards a user would like to draw from the deck

shuffled_deck = response.json() # shuffled_deck is a dictionary containing the json response of the api call

deck_id = shuffled_deck['deck_id'] # deck_ip is a variable that contains the value of the deck_id key in shuffled_deck

url = 'https://deckofcardsapi.com/api/deck/' + deck_id + '/draw/?count=' + card_count # url has been changed to call the draw parameter of the
                                                                                      # api and use the deck id of the shuffled deck and the 
payload={}                                                                            # number stored in card_count as the ammount of cards to 
headers = {}                                                                          # be drawn

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text) # the json response will print showing the cards that were drawn using the passed parameters




# Question 8



import requests   


def gameRules():  # function responsible for displaying print statements listing game rules before starting game 

    print('Welcome to virtual war. This game is played against a computer which will draw the same ammount of cards as you from 0-5 cards.')
    print('Specify the number of cards when prompted. The number cards are face value while all other cards are worth 10 points. \n')  


def userInput(prompt, answerList): # User input function

    answer = input(prompt) # variable that tracks the users input according to the prompt that was passed to the function

    while answer not in answerList: # while loop that will return the initial inpuy prompt if the users answer is not valid 
        print('Please respond using a valid answer.')
        answer = input(prompt)
    
    return answer #The answer will be returned once a valid answer is entered



def getDeck(): #function responsible for getting the new deck from api
    
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1" # url specifies the destination url for the api call  

    payload= {} # payload and headers are empty dictionaries responsible for occupying the data and header parameters respectively
    headers = {} 

    response = requests.request("GET", url, headers=headers, data=payload)  # response is a variable that is calling a http get request using the 
                                                                            # request library with the url variable as the destination url, and the
                                                                            # headers and payload dictionaries as the headers and data parameters.

    
    deckDictionary = response.json() # deckDictionary returns a dictionary containing the results of the api call from the response variable

    deckID = deckDictionary['deck_id']

    
    return deckID # deckID is returned for further use



def drawFromDeck(cardNum, deckID):  # function responsible for drawing the number of cards in the deck

    count = 0 # count is used to later determine which card the for loop is on

    cardCount = str(cardNum)
    
    url = 'https://deckofcardsapi.com/api/deck/' + deckID + '/draw/?count=' + cardCount # url specifies the destination url for the api call
                                                                                        # using the variables passed through the function to
                                                                                        # determine which deck the api should use and how many
                                                                                        # cards to draw
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)  # response is a variable that is calling a http get request using 
                                                                            # the request library with the url variable as the destination url, and
                                                                            # the headers and payload dictionaries as the headers and data 
                                                                            # parameters
                                                                            
    cardsDrawn = response.json()   # cardsDrawn returns a dictionary containing the results of the api call from the response variable                       

    cardValue = [] # cardValue is an empty list which will contain the value of each card drawn 
    
    for card in cardsDrawn['cards']: # the for loop will go through each card in the response dictionary and add 1 to the count, the count number will
                            # be used to tell the user which card is being displayed and what the value and suit is for said card, then said
                            # card will be added to the cardValue list to be further utilized
        count += 1

        print('Card # ' + str(count) + ' is the ' + card['value'] + ' of ' + card['suit'])

        cardValue.append(card['value'])

    
    return cardValue # the list of card values is returned to main



def calculateValue(cardsList): #function responsible for calculating card value

    royalList = ['ACE','QUEEN','JACK','KING'] # royalList contains all of the non numbered cards as they appear in the json response

    
    for card in cardsList: # for loop iteratesd through the  list of cards that has been passed to the function
    
        if card in royalList:               # if the list of cards contains any of the values in the royal list, the royalIndex variable will 
                                                # use the index function to search for the card in the list and replace it with the integer 10
            royalIndex = cardsList.index(card)  # otherwise the index variable will act in a similar fashion for all other cards, except that
                                                # the value of the card will be replaced with the integer value of itself
            cardsList[royalIndex] = int('10')

        else:
            
            index = cardsList.index(card)

            cardsList[index] = int(card)

            card = int(card)
            
    valueSum = sum(cardsList) # valueSum will add all of the cards in the cardsList together to get a single value
    
    return valueSum # valueSum is returned to main for further use




#main code



gameRules() # the gameRules() function is called before the start of the game to explain the game rules           
cardPrompt = userInput('How many cards would you like to draw? (0-5): ', ['0','1','2','3','4','5']) # the cardprompt variable calls the userInput
                                                                                                # function to get a number of cards from the user

cardNum = int(cardPrompt) # cardNum turns the value given by cardPrompt into a integer for further use


if cardNum == 0:  # if the player has selected zero cards then a statement will print stating that there was no game played and the program ends
    print('No cards were drawn, no game was played.')

if cardNum <= 5 and cardNum != 0: # if the player picks a card value from 1-5 then the game will commence as follows
          gameDeck = getDeck()    # gameDeck calls the getDeck function which calls to the api for a new deck and returns the deck id to main
          
          print('Your deck has been shuffled. \n') # a print statement declares that the deck has been shuffled by the api
          
          userDraw = drawFromDeck(cardNum, gameDeck) # userDraw calls the drawFromDeck function which  will draw the specified number of cards
                                                     # from the cardNum variable and use the deck id returned from the gameDeck variable
          
          userScore = calculateValue(userDraw) # userScore calls the calculateValue function and passes the list of cards returned from userDraw

          print('Your total score is: ', userScore, '\n') # a print statement will list the users score and announce the start of the computers
          print('Now the computer will draw \n')          # drawing sequence

          cpuDraw = drawFromDeck(cardNum, gameDeck) # cpuDraw calls the drawFromDeck function using the same deck id and number of cards as userDraw

          cpuScore = calculateValue(cpuDraw) # cpuScore calls the calculateValue function to score the computer's cards that are returned in the
                                             # cpuDraw function
          print('The computers total score is: ', cpuScore, '\n') # the print statement shows the computer's total score

         # three if statements will compare the value of the game and announce either a winner or tie based on the values of userScore and cpuScore
          if userScore > cpuScore:
             print('You won the war against the computer player!')

          if userScore < cpuScore:
             print('You lost the war against the computer player!')

          if userScore == cpuScore:
             print('The war between you and the computer ended in a tie!')


















