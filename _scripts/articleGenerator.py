#!/usr/bin/python

import sys
import getopt
import re
import requests
import json
import time
import shutil


anchor_tag = '<a\n\tclass="accented-link external-card-link"\n\ttarget="_blank"\n\thref="{0}"\n\tdata-toggle="popover"\n\tdata-placement="top"\n\tdata-content="<img src=\'{1}\' width=100% height=100%>">\n\t{2}\n</a>'

pictures_tag = '{{% include pics.html\n{0} %}}\n<br />'

single_picture_tag = 'pic1="{0}"\nstyle="single"\nwidth="33%"'

# returns a 2-element array with card uri on scryfall, and the image uri


def get_card_data(name):
    card_uri = ''
    image_uri = ''
    try:
        url = "https://api.scryfall.com/cards/search?q=!\"{0}\"".format(name)
        # print(url)
        r = requests.get(url)
        #print("request got")
        x = json.loads(r.text)
        card = x["data"][0]
        card_uri = card["scryfall_uri"]
        # picking image src based on existance of MDFCs
        if 'image_uris' in card:
            image_uri = card["image_uris"]["normal"]
        else:
            front_card = card["card_faces"][0]
            back_card = card["card_faces"][1]
            if front_card["name"] == name:
                image_uri = front_card["image_uris"]["normal"]
            else:
                image_uri = back_card["image_uris"]["normal"]
    except:
        print("ERROR PROCESSING: " + name)
    # prevent bothering scryfall too much
    time.sleep(.15)
    return [card_uri, image_uri]


def format_line(line):
    result = ''
    # check to see if line even has any cards in it. Otherwise just return
    if "[[" in line:
        card_count = line.count("[[")
#        print('card count: '+str(card_count))
        for n in range(card_count):
            card_name = re.search("\[\[(.*?)\]\]", line).group(1)
#            print('card name found: '+str(card_name))
            card_data = get_card_data(card_name)
            card_tag = anchor_tag.format(card_data[0], card_data[1], card_name)
            line = re.sub("\[\[(.*?)\]\]", card_tag, line, 1)
        #result = line.replace('[[', begin_tag).replace(']]', end_tag)
        result = line
    else:
        result = line
    # Checks for cards that will use our picture includes
    if "((" in line:
        pictures_count = line.count("((")
        for n in range(pictures_count):
            card_names = re.search("\(\((.*?)\)\)", line).group(1)
#           print('card names found: '+str(card_names))
            cards = card_names.split(";")
            card_uris = []
            for card in cards:
                card_data = get_card_data(card)
                card_uris.append(card_data[1])

            card_pics = ""
            card_count = len(card_uris)
            if card_count == 1:
                card_pics = single_picture_tag.format(card_uris[0])
            else:
                for pic_number in range(len(card_uris)):
                    card_pic = 'pic{0}="{1}"\n'.format(
                        pic_number+1, card_uris[pic_number])
                    card_pics += card_pic
            # print(card_pics)
            cards_include = pictures_tag.format(card_pics)
            line = re.sub("\(\((.*?)\)\)", cards_include, line, 1)
        result = line
    else:
        result = line

    return result


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('Error: articleGenerator.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('articleGenerator.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print('Input file is ' + inputfile)
    # strip file location of article name
    outputfile = inputfile.split("_posts/")[1]
    # strip file extension and add identifier
    outputfile = (outputfile.split(".")[0] + "_formatted.md")
    print('Output file is '+outputfile)
    # proceed to read input file
    input_file = open(inputfile, "r")
    output_file = open(outputfile, "w")
    for line in input_file:
        output_file.write(format_line(line))
    input_file.close()
    output_file.close()
    # move to correct directory
    shutil.move(outputfile, '../_posts')


if __name__ == "__main__":
    main(sys.argv[1:])
