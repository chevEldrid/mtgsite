import shutil
import os

def main():
    print("The low budget file shuffling cousin!")
    # clear out old brewcrew
    SITE_DIRECTORY = '../../brewcrew'

    for filename in os.listdir(SITE_DIRECTORY):
        file_path = os.path.join(SITE_DIRECTORY, filename)
        try:
            if filename != "CNAME" and filename != '.gitignore': #special exception to keep the one file we need
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    if filename != ".git": #can't get rid of git...
                        shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Brewcrew successfully cleared! Proceeding to copy _site directory...")

    source = '../_site/'
    dest1 = SITE_DIRECTORY
    files = os.listdir(source)
    for f in files:
        shutil.move(source+f, dest1)

    print("Site moved successfully!")

if __name__ == '__main__':
    main()