$(function () {
  // Current user
  if ($("#current-user").length) {
    const currentUser = localStorage.getItem("me");
    if (currentUser) {
      $("#logout-button").show();
      var data = JSON.parse(currentUser);
      $("#welcome-user").text("Hi, " + data.name);
      $("#logout-button").click(function() {
        localStorage.removeItem('me');
        window.location.href = "/";
      })
    } else {
      $("#logout-button").hide();
    }
  }
});
