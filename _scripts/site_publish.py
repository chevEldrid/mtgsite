import shutil
import os


def string_contained(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False


def sanityCheckConfirmation():
    noAnswer = True
    confirmed = False

    while noAnswer:
        print("Just for sanity's sake, did you....[y/n]")
        print("- Remember to update the media.yml with any new videos released?")
        confirmation = str(input())
        if confirmation[0].upper() == "Y":
            print("Excellent, we proCEED!")
            noAnswer = False
            confirmed = True
        elif confirmation[0].upper() == "N":
            print("Get on that ish!!")
            noAnswer = False
        else:
            print("input not understood, we try again...")
    return confirmed


def main():
    print("The low budget file shuffling cousin!")
    source = '../_site/'
    # ID for google analytics, should only be present in production
    PRODUCTION_TEST_STRING = 'UA-180984713-1'
    # check if the site directory is with a production build...
    site_index_file = source+'index.html'
    if not string_contained(site_index_file, PRODUCTION_TEST_STRING):
        print('Production test string was not found in _site index file...this might be a dev build\nExiting.')
        exit(0)
    if not sanityCheckConfirmation():
        print('Publishing Script exiting, fix the sanity check to continue')
        exit(0)
    # clear out old hexdrinkers directory
    SITE_DIRECTORY = '../../hexdrinkers'

    for filename in os.listdir(SITE_DIRECTORY):
        file_path = os.path.join(SITE_DIRECTORY, filename)
        try:
            if filename != '.gitignore':  # special exception to keep the one file we need
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    if filename != ".git":  # can't get rid of git...
                        shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Hexdrinkers successfully cleared! Proceeding to copy _site directory...")

    dest1 = SITE_DIRECTORY
    files = os.listdir(source)
    for f in files:
        shutil.move(source+f, dest1)

    print("Site moved successfully!")


if __name__ == '__main__':
    main()
