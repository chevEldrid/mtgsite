#!/usr/bin/python

import getopt
import os
import sys

OLD_SCRYFALL_URL = 'https://img.scryfall.com/cards'
NEW_SCRYFALL_URL = 'https://c1.scryfall.com/file/scryfall-cards'


def updateArticle(fileName, inputFolder, clean):
    filepath = os.path.join(inputFolder, fileName)
    print('Updating ' + fileName)

    inputFile = open(filepath, "r")
    outputFile = open(filepath+'_formatted.md', "w")
    anchorTag = ''

    for line in inputFile:
        # using the syntax of our articleGenerator to find cases where anchor tags are added
        if clean and ("<a" in line and "</a>" not in line):
            prevLine = line.rstrip()
            anchorTag = anchorTag + line.rstrip()
            for anchorDescription in inputFile:
                anchorTag = anchorTag + anchorDescription.rstrip()
                if "</a>" in anchorDescription and 'data-content' in anchorTag:
                    cardName = "[[{0}]]".format(prevLine.strip())
                    outputLine = anchorDescription.replace("</a>", cardName, 1)
                    outputFile.write(outputLine)
                    anchorTag = ''
                    break
                prevLine = anchorDescription.rstrip()
        # replace all instances of old scryfall url with new one
        # hypothetically, this could be the entire answer
        elif OLD_SCRYFALL_URL in line:
            newLine = line.replace(OLD_SCRYFALL_URL, NEW_SCRYFALL_URL)
            outputFile.write(newLine)
        else:
            outputFile.write(line)

    inputFile.close()
    outputFile.close()
    # rename new file to replace old
    oldVersion = os.path.join(
        inputFolder, (fileName.split(".")[0] + "_old.md"))
    newVersion = os.path.join(
        inputFolder, (fileName + "_formatted.md"))
    os.rename(filepath, oldVersion)
    os.rename(newVersion, filepath)


def main(argv):
    inputFolder = ''
    clean = False  # setting to true removes anchor tags from articles and 'cleans' them
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifolder="])
    except getopt.GetoptError:
        print('Error: articleGenerator.py -i <inputfolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('articleGenerator.py -i <inputfolder>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            inputFolder = arg
        elif opt == '-c':
            clean = True
    print('Input inputFolder is ' + inputFolder)
    for fileName in os.listdir(inputFolder):
        updateArticle(fileName, inputFolder, clean)


if __name__ == "__main__":
    main(sys.argv[1:])
