# Welcome to the README!

This repo serves as the development environment for [Hexdrinkers.com](https://hexdrinkers.com). while the [Hexdrinkers](https://github.com/chevEldrid/hexdrinkers) repo contains the code that's actually pushed to github pages, this separation allows us to maintain a separate environment to test changes locally and an additional step before code is automatically merged to master.

Hexdrinkers.com runs on Jekyll, a static site generator that integrates directly with github pages for easy releasing. You can find all the custom jekyll formatting we do for articles, series, etc in the "\_includes" and "\_layouts" directories.

Custom ruby plugins live in the "\_plugins" directory, but so far there hasn't really been a need for any.

The bulk of custom programming lives in the "\_scripts" directory. These are custom python scripts for site pre and post processing, handling everything from pulling articles into the site's architecture from The Hexdrinkers' google drive, to putting the production-ready site directory into our production repo.
The biggest benefit however comes from the "articleGenerator.py" program that integrates directly with a 3rd-party api to pull card information and properly format articles with custom anchor tags, hyperlinks, and embedded pictures based on provided text. This script alone has knocked the time it takes to take a finished article and have it running on the live site from 30 minutes to 5.

## Site Scripts

While having a completely custom site does make certain things easier, like complete code control and design, it does leave a little to be desired in terms of automation of posting, formatting, and serving. The current Hexdrinkers team has two content creators without a background in computer science, meaning the final production of all articles and site content is bottlenecked by requiring direct action from a single individual. These scripts allow us to transform articles from the form non-cs writers are comfortable with, to the markdown files that populate the site in a fraction of the time it would take otherwise.

### article_pull.py

```
python article_pull.py
```

Once you've authenticated with Google Drive (and have their drive api tools installed, as well as the json secrets), this script will pull all articles published to the "articles.md" folder since the date of "changelog.txt" and put them in the \_posts folder. Therefore. you NEED to have the secrets and a changelog.txt with a date for this to work.

### articleGenerator.py

```
python articleGenerator.py -i [path/to/article]
```

ArticleGenerator replaces two types of regex patterns with properly formatted data:

- mtg cardnames surrounded by [[brackets]] will be replaced with an appropriate anchor tag and hover link, sourced from Scryfall.
- cardnames surrounded by {{curly; braces}} will be transformed into embedded images, also sourced from Scryfall. Max: 3 images separated by semicolons
  If a name isn't found in either case, articleGenerator creates an empty tag for you to fill in. Then the formatted article is placed in the appropriate \_posts directory.

### site_publish.py

```
python site_publish.py
```

Saves time with moving all the production files from \_site into the production repo, hexdrinkers. This also makes sure you won't accidentally delete any necessary files (cname) required in the destination directory.
Hexdrinkers is the repo actually hooked up to github pages for publishing. The main requirement for this script to work is the hexdrinkers repo MUST be at the same level as this one.

## Install Guides

All members of the Hexdrinkers have this repo on their own machines to run locally and check how an article file will look on the finished site. This helps IMMENSELY in terms of what the final person has to do to format the articles since they should already be in a production-ready form sans images and links. This part of the repo serves as a reminder for what process to take to run the site locally.

### Windows

- You'll want to enable Linux subsystem for Windows, Here's a guide from [windowscentral](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10)

### Less-cs familiar Hexdrinkers

- Clone this repo using your Linux Terminal.
- MTGSite is built using jekyll, which is a Ruby gem. You'll need Ruby in order for this to work so you'll need to confirm you have Ruby installed and then navigate to the mtgsite directory. If you don't have ruby installed, check [here](https://linuxize.com/post/how-to-install-ruby-on-debian-9/)
- run 'bundle install' in the command line to install the necessary ruby gems and packages that make mtgsite run. Primarily, this is going to be Jekyll and its associated plugins
- finally, run 'bundle exec jekyll serve' to start up the local server and voila! You're all set! You should see the dev version of this site at localhost://4000
- for the production version, the command is 'JEKYLL_ENV=production bundle exec jekyll build' This creates a copy of the production code in the \_site directory, which is used to port to "hexdrinkers". The production flag tells Jekyll to generate code including google analytics information and comment blocks
