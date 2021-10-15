var BASE_URL = "http://localhost:8080/api";

Date.prototype.toJSONLocal = (function () {
  function addZ(n) {
    return (n < 10 ? "0" : "") + n;
  }
  return function () {
    return (
      this.getFullYear() +
      "-" +
      addZ(this.getMonth() + 1) +
      "-" +
      addZ(this.getDate()) +
      "T" +
      addZ(this.getHours()) +
      ":" +
      addZ(this.getMinutes()) +
      ":" +
      addZ(this.getSeconds())
    );
  };
})();

function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1),
    sURLVariables = sPageURL.split("&"),
    sParameterName,
    i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split("=");

    if (sParameterName[0] === sParam) {
      return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
    }
  }
  return false;
}

function calculateHt(val) {
  if (val.length > 0) {
    if (val.includes("Ht")) {
      return parseInt(val.replace("Ht", "").replace(".", "").replace(",", "").replace(/ /g, ""));
    }
    if (parseInt(val) > 0) return val;
  }

  return "";
}

function calculateDiameter(val) {
  if (val.length > 0) {
    if (val.includes("Diam")) return val.replace("Diam.", "").replace(/ /g, "");
    if (parseInt(val) > 0) return val;
  }

  return "";
}

$(function () {
  // Enable Semantic UI
  if ($(".ui.checkbox").length) $(".ui.checkbox").checkbox();
  if ($(".ui.dropdown").length) $(".ui.dropdown").dropdown({ on: "hover" });
  if ($(".main.menu").length) {
    // fix main menu to page on passing
    $(".main.menu").visibility({
      type: "fixed",
    });
    $(".overlay").visibility({
      type: "fixed",
      offset: 80,
    });
  }

  // Check if user logged in, redirect to home screen
  var path = window.location.pathname;
  const currentUser = localStorage.getItem("me");
  if (path !== "/register.html") {
    if (path == "/" || path == "/index.html") {
      if (currentUser) {
        location.href = "/home.html";
      }
    } else {
      if (!currentUser) {
        location.href = "/";
      }
    }
  }

  // Update user name on menu
  var userData = JSON.parse(currentUser);
  if (currentUser) {
    if (userData.role != "admin") {
      $("#users-menu").hide();
    }

    $("#user-name-menu").text(userData.name);
    $("#logout-button").click(function () {
      localStorage.removeItem("me");
      window.location.href = "/";
    });
    $("#edit-button").click(function () {
      window.location.href = "/edit-profile.html";
    });
  }

  function deleteResource(id, callback) {
    var r = confirm("Are you sure you want to delete this record?");
    if (r == true) {
      $.ajax({
        type: "DELETE",
        url: BASE_URL + "/resources/" + id,
        success: function () {
          if (callback) callback();
        },
      });
    }
  }

  // Resource list
  if ($("#resource-list").length) {
    // Hide add button if not admin
    const currentUser = JSON.parse(localStorage.getItem("me"));
    const isAdmin = currentUser.role === "admin";
    if (!isAdmin) $("#add-resource").hide();

    // Page calculate
    var currentPage = parseInt(getUrlParameter("page")) || 1;
    var currentSearch = getUrlParameter("q") || '';

    function queryPaging(search, page) {
      $.ajax({
        type: "GET",
        url: BASE_URL + "/resources?pageSize=15&pageNo=" + Math.max(0, page - 1) + "&q=" + search,
        success: function (result) {
          if (result.status === 200) {
            // Success
            var data = result.data;
            var pageCount = result.pageCount;
            var list_html = "";

            for (var i = 0; i < data.length; i++) {
              var item = data[i];

              list_html += '<tr class="resource-item" id="resource-' + item.id + '">';
              list_html += "<td>" + item.id + "</td>";
              list_html +=
                '<td><img class="ui image tiny" src="' +
                (item.imageUrl || "./assets/images/banner-1.png") +
                '" alt="" /></td>';
              // = Body
              list_html += "<td class='bold'>" + (item.location || "N/A") + "</td>";
              list_html += "<td>" + (item.catalogue || "N/A") + "</td>";
              list_html +=
                "<td>" + (item.plate ? item.plate.trim().replace("PLATE", "").replace(/ /g, "") : "N/A") + "</td>";

              // == Height
              list_html += "<td>";
              if (calculateHt(item.height)) list_html += calculateHt(item.height) + " cm";
              else list_html += "-";
              list_html += "</td>";

              // == Diameter
              list_html += "<td>";
              if (calculateDiameter(item.diameter).length > 0) list_html += calculateDiameter(item.diameter);
              else list_html += "-";
              list_html += "</td>";

              list_html += "<td> <a href='/resource-details.html?id=" + item.id + "'>View</a> </td>";

              list_html += "</td>";
              list_html += "</tr>";
            }
            $("#resource-list").html(list_html);
            console.log(page, pageCount)
            // Pagination
            $("#current-page").html(page + " of " + pageCount);
            if (page < pageCount && pageCount > 1) {
              var nextPage = page + 1;
              $("#next-page").removeClass("disabled");
              $("#next-page").attr("href", "resource-list.html?page=" + nextPage + "&q=" + search);
              $("#last-page").removeClass("disabled");
              $("#last-page").attr("href", "resource-list.html?page=" + pageCount + "&q=" + search);
            }

            if (page == pageCount) {
              $("#next-page").addClass("disabled");
              $("#last-page").addClass("disabled");
            }

            if (page == 1) {
              $("#prev-page").addClass("disabled");
              $("#first-page").addClass("disabled");
            }

            if (page > 1 && pageCount > 1) {
              var prevPage = page - 1;
              $("#prev-page").removeClass("disabled");
              $("#prev-page").attr("href", "resource-list.html?page=" + prevPage + "&q=" + search);
              $("#first-page").removeClass("disabled");
              $("#first-page").attr("href", "resource-list.html?page=1" + "&q=" + search);
            }

            // Delete function
            $(".resource-list-item-delete").click(function (event) {
              event.preventDefault();
              deleteResource(event.target.id, function () {
                $("#resource-" + event.target.id).remove();
              });
            });
          } else {
            // Error
            $("#resource-list").empty().addClass("error").append(result.data);
          }
        },
      });
    }

    queryPaging(currentSearch, currentPage);

    // Search in resource list
    $("#resource-search-input").val(currentSearch)
    $("#resource-search-input").on("input", function () {
      var dInput = this.value.toUpperCase();

      queryPaging(dInput, 1);
    });
  }

  // Resource details
  if (path.includes("/resource-details.html")) {
    var id = getUrlParameter("id");

    // Hide add, delete button if not admin
    const currentUser = JSON.parse(localStorage.getItem("me"));
    const isAdmin = currentUser.role === "admin";
    if (!isAdmin) {
      $("#resource-delete-btn").hide();
      $("#resource-edit-btn").hide();
    }

    // Edit button href modify
    $("#resource-edit-btn").attr("href", "resource-new.html?id=" + id);

    // Add click event for delete button
    $("#resource-delete-btn").click(function (e) {
      e.preventDefault();
      deleteResource(id, function () {
        location.href = "/resource-list.html";
      });
    });

    $.ajax({
      type: "GET",
      url: BASE_URL + "/resources/" + id,
      success: function (result) {
        if (result.status === 200) {
          // Success
          var data = result.data;

          $("#resource-location").val(data.location);
          $("#resource-catalogue").val(data.catalogue || "N/A");
          $("#resource-height").val(calculateHt(data.height) || "N/A");
          $("#resource-diameter").val(calculateDiameter(data.diameter) || "N/A");
          $("#resource-plate").val(data.plate.replace("PLATE", "").replace(/ /g, "") || "N/A");
          $("#resource-description").val(data.description);
          $("#resource-note").val(data.note || "-");
          $("#resource-image").attr("src", data.imageUrl || "./assets/images/banner-1.png");
        } else {
          // Error
          $("#resource-detail").empty().addClass("error").append(result.data);
        }
      },
    });
  }

  // Resource edit & create
  if (path.includes("/resource-new.html")) {
    $("#imageUrl").on("input", function () {
      var dInput = this.value;
      $("#resource-image").attr("src", dInput);
    });

    var id = getUrlParameter("id");

    if (id) {
      $("#page-title").text("Edit resource");
      $.ajax({
        type: "GET",
        url: BASE_URL + "/resources/" + id,
        success: function (result) {
          if (result.status === 200) {
            // Success
            var data = result.data;

            $("#location").val(data.location);
            $("#catalogue").val(data.catalogue);
            $("#height").val(data.height);
            $("#diameter").val(data.diameter);
            $("#plate").val(data.plate);
            $("#imageUrl").val(data.imageUrl);
            $("#description").val(data.description);
            $("#note").val(data.note);
            $("#resource-image").attr("src", data.imageUrl);
          } else {
            alert("Cannot get resource detail");
          }
        },
      });

      $("#resource-new-form")
        .form({
          fields: {
            location: "empty",
            catalogue: "empty",
          },
        })
        .api({
          url: BASE_URL + "/resources/" + id,
          method: "PUT",
          beforeXHR: (xhr) => {
            xhr.setRequestHeader("Content-Type", "application/json");
          },
          beforeSend: (settings) => {
            var fields = $(this).form("get values");
            settings.data = JSON.stringify({
              location: fields.location,
              catalogue: fields.catalogue,
              height: fields.height || "",
              diameter: fields.diameter || "",
              plate: fields.plate || "",
              description: fields.description || "",
              note: fields.note || "",
              imageUrl: fields.imageUrl || "",
            });
            return settings;
          },
          onSuccess: function (result) {
            if (result.status !== 200) {
              $(this).form("add errors", [result.data]);
            } else {
              window.location = "/resource-list.html";
            }
          },
          onFailure: function (error, fields) {
            // invalid response
            console.log("err", fields);
            $(this).form("add errors", [error.message]);
          },
        });
    } else {
      $("#resource-new-form")
        .form({
          fields: {
            location: "empty",
            catalogue: "empty",
          },
        })
        .api({
          url: BASE_URL + "/resources",
          method: "POST",
          beforeXHR: (xhr) => {
            xhr.setRequestHeader("Content-Type", "application/json");
          },
          beforeSend: (settings) => {
            var fields = $(this).form("get values");
            settings.data = JSON.stringify({
              location: fields.location,
              catalogue: fields.catalogue,
              height: fields.height || "",
              diameter: fields.diameter || "",
              plate: fields.plate || "",
              description: fields.description || "",
              note: fields.note || "",
              imageUrl: fields.imageUrl || "",
            });
            return settings;
          },
          onSuccess: function (result) {
            if (result.status !== 200) {
              $(this).form("add errors", [result.data]);
            } else {
              window.location = "/resource-list.html";
            }
          },
          onFailure: function (error, fields) {
            // invalid response
            console.log("err", fields);
            $(this).form("add errors", [error.message]);
          },
        });
    }
  }
});
