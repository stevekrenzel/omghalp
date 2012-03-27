if($('[name="results"]').length > 0) {
  $('body').scrollTop($('[name="results"]').position().top);
}

// If a person keeps typing in a single input field, this will propogate those
// characters to the neighboring input fields.
var autotype = function() {
  var current = $(this);

  // We wait until next tick so that the value of the element is up to date.
  setTimeout(function() {
    if(current.val().length > 1) {
      var suffix = current.val().substring(1);
      var next = current.next('.char');
      current.val(current.val()[0]);
      for(var i = 0; i < suffix.length; i++) {
        while(next.length > 0) {
          if(next.val().length == 0) {
            next.val(suffix[i]);
            break;
          }
          next = next.next('.char');
        }
      }
    }
  }, 0);
}

$('.char').keypress(autotype);
$('.char').change(autotype);
$('.char').focus(function() { $(this).select(); });
