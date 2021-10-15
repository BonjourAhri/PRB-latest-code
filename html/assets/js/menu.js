$(document).ready(function(){
  var url = (window.location != window.parent.location)
            ? document.referrer
            : document.location.href;
  var current = url.replace(/^[^:]+:\/\/[^/]+/, '').replace(/#.*/, '').split('?')[0];

  $('#top-menu-nav ul li a').each(function() {
      var $this = $(this);
      
      // if the current path is like this link, make it active
      if($this.attr('href').indexOf(current) !== -1) {
          $this.closest( "li" ).addClass('selected');
      }
  })

  const currentUser = localStorage.getItem("me");
  if (currentUser) {
    var data = JSON.parse(currentUser)
    if (data.role !== 'admin') {
      $("#users-menu").hide();
    }
  }
})