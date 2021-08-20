# Welcome to the README!

## Site Scripts

While having a completely custom site does make certain things easier, like complete code control and design, it does leave a little to be desired in terms of automation of posting, formatting, and serving. That's where our squad of super scripts comes in.

### article_pull.py

```
python article_pull.py
```

Once you've authenticated with Google Drive (and have their drive api tools installed, as well as the json secrets which Chev can share), this script will pull all articles published to the "articles.md" folder since the date of "changelog.txt" and put them in the \_posts folder. Therefore. you NEED to have the secrets and a changelog.txt with a date for this to work.

### articleGenerator.py

```
python articleGenerator.py -i [path/to/article]
```

Our oldest file, articleGenerator currently just replaces all magic cards with [[brackets]] with the appropriate anchor tag. If a name isn't found, it creates an empty anchor tag for you to fill in. Then the formatted article is placed in the appropriate \_posts directory.

### site_publish.py

```
python site_publish.py
```

Simply moves all files and folders in the \_site folder to the hexdrinkers folder in the same directory. hexdrinkers is the repo actually hooked up to github pages. it NEEDS to be in the same directory. pls.

## Install Guides

### Windows

- Most likely you want to enable Linux subsystem for Windows, which you can do any number of ways I can't remember

### Everyone

- Then clone the repo using your Linux Terminal.
- The project's in Ruby so you'll need to confirm you have Ruby installed and navigate to the mtgsite directory
- run 'bundle install' in the command line to install the necessary ruby tools
- finally, run 'bundle exec jekyll serve' to start up the server and voila! You're all set! You should see it at localhost://4000
- to get the production version of the site (chev) run
