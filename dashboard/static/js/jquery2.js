function getSize() {
  size = $( "#font-size" ).css( "font-size" );
  size = parseInt(size, 10);
  $( "#font-size" ).text(  size  );
}

//get inital font size
getSize();

$( "#up" ).on( "click", function() {

  // parse font size, if less than 50 increase font size
  if ((size + 2) <= 50) {
    $( "#font-size" ).css( "font-size", "+=2" );
    $( "#font-size" ).text(  size += 2 );
  }
});

$( "#down" ).on( "click", function() {
  if ((size - 2) >= 12) {
    $( "#font-size" ).css( "font-size", "-=2" );
    $( "#font-size" ).text(  size -= 2  );
  }
});