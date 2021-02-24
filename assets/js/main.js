//create the hover ability for cards
$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        html : true,
        trigger : 'hover'
    });
    footer_saying();
});

//hardcoded functions that allow the mobile navbar to open and close
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

function footer_saying() {
  let sayings = [
    'Interestingly, you can also apply the Ballmer Peak Principle to MTG with fantastic results.',
    'Sometimes you have to let the Omniscience resolve. For science.',
    'If you see Kenrith in Brawl, you\'re going to need a bigger beer.',
    'What do Oliver Twist, the Combat Step, and Beer all have in common? “Please sir, may I have another?”',
    'Fun Vorthos Fact: Kozilek is a big Appletini Guy.',
    'Your max handsize is only seven if somebody notices.',
    'People who tap their lands at a 45 degree angle are up to something.',
    'Lands in the front, horses in the back.',
    'A commander deck only needs more than 32 lands if you\'re a coward.',
    'Life, Liberty, and the pursuit of mana',
    'Fun challenge: Play decks worth less than the cost of beer and food for the evening',
    'Print Return to Kamigawa or we\'ll make it ourselves',
    'Wizards, we know green is the best, but keep it on the DL. Everyone\'s starting to notice...',
    'Math is for blockers',
    'Winner of the first game controls the aux'
  ];
  let population = sayings.length;
  let saying_index = Math.floor(Math.random() * population);     // returns a random integer from 0 to length of sayings
  document.getElementById("footerSaying").innerHTML = sayings[saying_index].italics();
}