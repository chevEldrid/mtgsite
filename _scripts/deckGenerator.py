#!/usr/bin/python

import sys
import getopt
import re
import requests
import json
import time
import shutil

# notes to future me
# figure out how to do multiple card copies. Thinking what we'll need is to make a card object that contains total number of copies that get added to cardTypes and cardTypes count
# ...dives into how many unique total - this way we'll have the number of cards necessary when reconstructing for the final html
# but don't forget, multiple copies doesn't mean multiple lines so there won't always be 100 cards listed. It's important for cards to know how many there are but that doesn't matter to putting it down on the sheet

# necessary html pieces
HTML_NAME = '<div class="text-center">\n<h3>{0}</h3></div>\n'
HTML_CONTAINER = '<div class="row">\n\t<div class="col-md-2"></div>\n<div class="col-md-8">\n<div class="row">\n\t{0}\n{1}\n</div>\n</div>\n</div>\n<br />\n<br />'
HTML_COLUMN = '<div class="col-6">{0}\n</div>'
HTML_TYPE = '<b>{0}</b>\n<p class="mb-0">\n{1}</p>\n'

CLASSES = ["Commander", "Sorcery", "Instant", "Artifact", "Creature",
           "Planeswalker", "Land", "Enchantment", "Unknown"]
TYPES = ["Commanders", "Sorceries", "Instants", "Artifacts", "Creatures",
         "Planeswalkers", "Lands", "Enchantments", "Unknowns"]
cards = {}
card_groups = []

# https://www.geeksforgeeks.org/subarray-whose-sum-is-closest-to-k/
# also don't forget, when adding brackets to a card name for articleGenerator, only put brackets around the card and not the number


class Card:
    def __init__(self, cardDetails):
        self.name = cardDetails[0]
        self.count = cardDetails[1]

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


def getCardType(name):
    if "*" in name:
        return "Commander"

    card_type = 'Unknown'
    try:
        url = "https://api.scryfall.com/cards/search?q=!\"{0}\"".format(name)
        # print(url)
        r = requests.get(url)
        #print("request got")
        x = json.loads(r.text)
        card = x["data"][0]
        type_line = card["type_line"]
        # picking the correct type
        card_types = type_line.split()
        # Special treatment for creatures
        if "Creature" in card_types:
            card_type = "Creature"
        else:
            for type in card_types:
                if type in CLASSES:
                    card_type = type
                    break

    except:
        print("ERROR PROCESSING: " + name)
    # prevent bothering scryfall too much
    time.sleep(.15)
    return card_type


# def cardnameAndCount(cardline):
#     words = cardline.split()
#     cardName = []
#     cardCount = 1
#     for word in words:
#         if bool(re.search(r'\d', word)):
#             cardCount = ''.join([i for i in word if i.isdigit()])
#             continue
#         if "*" in word:
#             continue
#         cardName.append(word)
#     return [" ".join(cardName), cardCount]

def getCardDetails(cardline):
    words = cardline.split()
    nameWords = []
    cardCount = 1
    isCommander = False
    cardType = "Unknown"
    for word in words:
        if bool(re.search(r'\d', word)):
            cardCount = ''.join([i for i in word if i.isdigit()])
            continue
        if "*" in word:
            isCommander = True
            continue
        nameWords.append(word)
    cardName = " ".join(nameWords)
    cardType = getCardType(cardName)
    return [cardName, cardCount, cardType, isCommander]


# count the number of cards of each type from input file
def tally_card_types(inputfile):
    cardCount = 0
    input_file = open(inputfile, "r")
    # cur_type = None
    for line in input_file:
        cur_word = line.rstrip()

        # cardLineDetails = cardnameAndCount(cur_word)
        # cardType = getCardType(cardLineDetails[0])
        cardDetails = getCardDetails(cur_word)
        cardType = cardDetails[2]
        if cardType not in cards.keys():
            cards[cardType] = CardType(TYPES[CLASSES.index(cardType)])

        # cards[cardType].add_card(Card(cardLineDetails))
        cards[cardType].add_card(Card(cardDetails))
        cardCount += 1
    input_file.close()
    return cardCount


def populateCardGroups():
    for key in cards:
        card_groups.append(cards[key])


def generateEvenColumnsHelper(i, halfDeck, memo):
    if i >= len(card_groups):
        return 1 if halfDeck == 0 else 0
    # <-- Check if value has not been calculated.
    if (i, halfDeck) not in memo:
        count = generateEvenColumnsHelper(i + 1, halfDeck, memo)
        count += generateEvenColumnsHelper(i + 1,
                                           halfDeck - card_groups[i].count(), memo)
        memo[(i, halfDeck)] = count  # <-- Memoize calculated result.
    return memo[(i, halfDeck)]     # <-- Return memoized value.


def generateEvenColumns(halfDeck, memo):
    subset = []
    otherSet = []
    for i, x in enumerate(card_groups):
        # Check if there is still a solution if we include cards[i]
        if generateEvenColumnsHelper(i + 1, halfDeck - x.count(), memo) > 0:
            subset.append(x)
            halfDeck -= x.count()
        else:
            otherSet.append(x)
    return [subset, otherSet]


# formating methods
def formatCardType(cardType):
    formattedCards = []
    for card in cardType.cards:
        formattedCards.append(card.formatted_name())
    cards = "\n<br />\n".join(formattedCards)
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
    # print decklist name to file
    output_file.write(HTML_NAME.format(deckTitle))
    # print decklist to file
    output_file.write(decklist)
    print("Printed to file successfully!")
    output_file.close()


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('Error: deckGenerator.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('deckGenerator.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print('Input file is ' + inputfile)
    outputfile = (inputfile.split(".txt")[0] + "_decked.txt")
    print('Output file is '+outputfile)
    cardCount = tally_card_types(inputfile)

    # check card types
    for card in cards:
        print(card + ": " + str(cards[card].count()))
    print("Total unique cards counted: " + str(cardCount))
    # its 10pm and I don't want to rewrite algorithm code for dictionaries, so making it back to an array
    populateCardGroups()

    print("And for my next trick...show you what card types should be on each side")
    halfDeck = int(cardCount / 2)
    print("trying with halfdeck size "+str(halfDeck))
    memo = dict()
    cardsSubset = generateEvenColumns(halfDeck, memo)

    # if it cannot divide equally, we need to run the program back with the minimum size of evenly distributed columns...
    # ...oooor hack it
    # UNTESTED - WILL SEE IF NECESSARY
    while(len(cardsSubset[0]) == 0):
        halfDeck -= 1
        memo = dict()
        cardsSubset = generateEvenColumns(halfDeck, memo)

    # attempt at creating proper formatted list - leggo
    decklist = formatContainer(cardsSubset[0], cardsSubset[1])
    printDeckToFile(outputfile, "YOUR DECK TITLE HERE!", decklist)
    print("Thank you, and goodnight")


if __name__ == "__main__":
    main(sys.argv[1:])
