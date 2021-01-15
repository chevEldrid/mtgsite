#!/usr/bin/python

import sys, getopt
import re
import requests
import json
import time
import shutil

TYPES = ["Sorceries", "Creatures", "Instants", "Artifacts", "Enchantments", "Planeswalkers", "Lands"]
cards = []

# https://www.geeksforgeeks.org/subarray-whose-sum-is-closest-to-k/
# also don't forget, when adding brackets to a card name for articleGenerator, only put brackets around the card and not the number

class CardType:
    def __init__(self, type):
        self.type = type
        self.cards = []

    def add_card(self, card):
        return self.cards.append(card)

    def count(self):
        return len(self.cards)

#count the number of cards of each type from input file
def tally_card_types(inputfile):
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
            cur_type.add_card(cur_word)
    input_file.close()

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
   tally_card_types(inputfile)

   #check card types
   print("Now...we see how many exists of each")
   for card in cards:
       print(card.type + ": ")
       print(card.count())


if __name__ == "__main__":
   main(sys.argv[1:])
