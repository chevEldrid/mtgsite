//create the hover ability for cards
$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        html : true,
        trigger : 'hover'
    });
});

//hardcoded functions that allow the mobile navbar to open and close
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}