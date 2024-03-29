---
author: chev
cover: assets/images/coverimage.jpg
youtube: https://www.youtube.com/watch?v=BSF5yoD-vC4
categories: [friendsWithBenefits, Brewday, Decktech]
tags: [commander, standard, vodka, whisky, beer]
title: Template
hook: "yipee kayay mother"
---

Welcome to our template post! This first paragraph will appear on the home page along with the cover image above.

The rest of this text will only appear on the actual page.

use this guide for formatting: https://www.markdownguide.org/basic-syntax/

embedded pictures follow syntax:
{% include pics.html pic1="/assets/images/RYE/rye1/rye1-1.png" }
This works for single pictures inline with article, or up to three pictures (generally cards) in a row across a page.

Here are two examples. The first will be a row of three cards across
{% include pics.html
pic1="https://img.scryfall.com/cards/large/front/d/5/d568c679-8421-4184-a73c-b18c4164fea5.jpg?1581479289"
pic2="https://img.scryfall.com/cards/large/front/9/e/9e97f8b1-01e9-42c3-af0d-05e861de82e5.jpg?1590106714"
pic3="https://img.scryfall.com/cards/large/front/a/1/a1ddd113-140f-49c9-b45c-cf1b0d1dffd8.jpg?1581478950" %}
(this works if you only include a pic1 or a pic1 and pic2. But you ALWAYS need a pic1)

This next example is for if you want a single image just ya know, stuck in there
{% include pics.html
pic1="https://img.scryfall.com/cards/large/front/d/2/d29ce094-e373-42b8-8540-8fde33f8a2a4.jpg?1590501450"
style="single"
width="33%" %}

You'll need to add the style="single" tag so our site knows to treat it right, and include a width for overall image size.

to add a link to a previous article do this:
[Selesnya Auras Brawl deck tech]({% post_url 2020/2020-05-14-brawldt_1 %}))

Oh, and while we're at it you can include any sort of html you want. markdown does its thing around it so

<p>this is totally legal</p>

all pictures you want to be popover links, write with double brackets like [[this]]
(our article pre-processor will convert that to anchor tags.)

Breakdown of the identifiers at the top of the page:
author - who wrote the thing
cover - link to the image you want as the cover art for the article.
youtube - IF this article is a companion piece to a stream, add link to vid here. Don't include otherwise
categories - what (if any) article series the post belongs to. Samples listed above
tags - the format and general beverage type associated with the article. Later, these will allow site viewers to view all articles that have to do with whisky, or standard, etc.
title - the short title of the article you want in the tab, and what shows on homepage
hook - text that appears on homepage to introduce the article

Sample decklist template to copy paste
