#!/usr/bin/python

import sys, getopt
import re
import requests
import json
import time
import shutil

#notes to future me
# figure out how to do multiple card copies. Thinking what we'll need is to make a card object that contains total number of copies that get added to cardTypes and cardTypes count 
# ...dives into how many unique total - this way we'll have the number of cards necessary when reconstructing for the final html
# but don't forget, multiple copies doesn't mean multiple lines so there won't always be 100 cards listed. It's important for cards to know how many there are but that doesn't matter to putting it down on the sheet

#necessary html pieces
HTML_NAME = '<div class="text-center">\n<h3>{0}</h3></div>\n'
HTML_CONTAINER = '<div class="row">\n\t<div class="col-md-2"></div>\n<div class="col-md-8">\n<div class="row">\n\t{0}\n{1}\n</div>\n</div>\n</div>'
HTML_COLUMN = '<div class="col-6">{0}\n</div>'
HTML_TYPE = '<b>{0}</b>\n<p class="mb-0">\n{1}</p>\n'

TYPES = ["Companion", "Commanders","Sorceries", "Creatures", "Instants", "Artifacts", "Enchantments", "Planeswalkers", "Lands"]
cards = []

# https://www.geeksforgeeks.org/subarray-whose-sum-is-closest-to-k/
# also don't forget, when adding brackets to a card name for articleGenerator, only put brackets around the card and not the number

class Card:
    def __init__(self, name, count):
        self.name = name
        self.count = count

    def formatted_name(self):
        number = (str(self.count) + "x")
        return (number + " [["+self.name+"]]")

class CardType:
    def __init__(self, type):
        self.type = type
        self.cards = []

    def add_card(self, card):
        return self.cards.append(card)

    def count(self):
        return len(self.cards)

def cardnameAndCount(cardline):
    words = cardline.split()
    cardName = []
    cardCount = 1
    for word in words:
        if bool(re.search(r'\d', word)):
            cardCount = ''.join([i for i in word if i.isdigit()])
            continue
        cardName.append(word)
    return [" ".join(cardName), cardCount]

#count the number of cards of each type from input file
def tally_card_types(inputfile):
    cardCount = 0
    input_file = open(inputfile, "r")
    cur_type = None
    for line in input_file:
        cur_word = line.rstrip()

        #if the line is a card type...
        # if line in TYPES:
        if cur_word in TYPES:
           #store current type if anything
           if cur_type is not None:
               cards.append(cur_type)
           cur_type = CardType(cur_word)
        else:
            cardDetails = cardnameAndCount(cur_word) 
            cur_type.add_card(Card(cardDetails[0], cardDetails[1]))
            cardCount += 1
    cards.append(cur_type)
    input_file.close()
    return cardCount

def generateEvenColumnsHelper(i, halfDeck, memo):
    if i >= len(cards): return 1 if halfDeck == 0 else 0
    if (i, halfDeck) not in memo:  # <-- Check if value has not been calculated.
        count = generateEvenColumnsHelper(i + 1, halfDeck, memo)
        count += generateEvenColumnsHelper(i + 1, halfDeck - cards[i].count(), memo)
        memo[(i, halfDeck)] = count  # <-- Memoize calculated result.
    return memo[(i, halfDeck)]     # <-- Return memoized value.

def generateEvenColumns(halfDeck, memo):
    subset = []
    otherSet = []
    for i, x in enumerate(cards):
    # Check if there is still a solution if we include cards[i]
        if generateEvenColumnsHelper(i + 1, halfDeck - x.count(), memo) > 0:
            subset.append(x)
            halfDeck -= x.count()
        else:
            otherSet.append(x)
    return [subset, otherSet]

##formating methods
def formatCardType(cardType):
    formattedCards = []
    for card in cardType.cards:
        formattedCards.append(card.formatted_name())
    cards="\n<br />\n".join(formattedCards)
    return HTML_TYPE.format(cardType.type, cards)

def formatCardColumn(cardColumn):
    formattedTypes = []
    for cardType in cardColumn:
        formattedTypes.append(formatCardType(cardType))
    column = "".join(formattedTypes)
    return HTML_COLUMN.format(column)

def formatContainer(columnOne, columnTwo):
    return HTML_CONTAINER.format(formatCardColumn(columnOne), formatCardColumn(columnTwo))

def printDeckToFile(outputfile, deckTitle, decklist):
    output_file = open(outputfile, "w")
    #print decklist name to file
    output_file.write(HTML_NAME.format(deckTitle))
    #print decklist to file
    output_file.write(decklist)
    print("Printed to file successfully!")
    output_file.close()


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print('Error: deckGenerator.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('deckGenerator.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print('Input file is '+ inputfile)
   outputfile = (inputfile.split(".txt")[0] + "_decked.txt")
   print('Output file is '+outputfile)
   cardCount = tally_card_types(inputfile)

   #check card types
   print("Now...we see how many exists of each")
   for card in cards:
       print(card.type + ": " + str(card.count()))
   print("Total cards counted: " + str(cardCount))
   
   print("And for my next trick...show you what card types should be on each side")
   halfDeck = cardCount / 2
   memo = dict()
   cardsSubset = generateEvenColumns(halfDeck, memo)
   for card in cardsSubset[0]:
       print(card.type + ": " + str(card.count()))
   print("...and for the other side...")
   for card in cardsSubset[1]:
       print(card.type + ": " + str(card.count()))

    #attempt at creating proper formatted list - leggo
   decklist = formatContainer(cardsSubset[0], cardsSubset[1])
   printDeckToFile(outputfile, "YOUR DECK TITLE HERE!", decklist)
   print("Thank you, and goodnight")

if __name__ == "__main__":
   main(sys.argv[1:])
