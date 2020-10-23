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

def main():
    print("The low budget file shuffling cousin!")
    source = '../_site/'
    PRODUCTION_TEST_STRING = 'UA-180984713-1' #ID for google analytics, should only be present in production
    # check if the site directory is with a production build...
    site_index_file = source+'index.html'
    if not string_contained(site_index_file, PRODUCTION_TEST_STRING):
        print('Production test string was not found in _site index file...this might be a dev build\nExiting.')
        exit(0)
    # clear out old hexdrinkers directory
    SITE_DIRECTORY = '../../hexdrinkers'

    for filename in os.listdir(SITE_DIRECTORY):
        file_path = os.path.join(SITE_DIRECTORY, filename)
        try:
            if filename != '.gitignore': #special exception to keep the one file we need
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    if filename != ".git": #can't get rid of git...
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