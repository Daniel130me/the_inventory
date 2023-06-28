toastr.options = {
  closeButton: false,
  debug: false,
  newestOnTop: false,
  progressBar: false,
  positionClass: "toast-bottom-right",
  preventDuplicates: true,
  onclick: null,
  showDuration: "300",
  hideDuration: "1000",
  timeOut: "5000",
  extendedTimeOut: "1000",
  showEasing: "swing",
  hideEasing: "linear",
  showMethod: "fadeIn",
  hideMethod: "fadeOut",
};

// slide in and out sidebar control starts here
$("#mobile-collapse1").click(function () {
  if (!$("#navbar_id").hasClass("mob-open")) {
    $("#navbar_id").addClass("mob-open");
    return false;
  }
});
$(".pcoded-main-container, .navbar").click(function () {
  if ($("#navbar_id").hasClass("mob-open")) {
    $("#navbar_id").removeClass("mob-open");
    return false;
  }
});
// slide in and out sidebar control ends here

$("#password1").keyup(function () {
  // $('input[type=password]').keyup(function() {
  var password = $(this).val();

  // Check if the password is at least 8 characters long.
  if (password.length < 8) {
    $(this).addClass("border-danger");
    $(this)
      .next(".password-strength")
      .text("Password must be at least 8 characters long.")
      .addClass("text-danger");
    return;
  }

  // Check if the password contains at least one uppercase letter.
  if (!/[A-Z]/.test(password)) {
    $(this).addClass("border-danger");
    $(this)
      .next(".password-strength")
      .text("Password must contain at least one uppercase letter.")
      .addClass("text-danger");
    return;
  }

  // Check if the password contains at least one lowercase letter.
  if (!/[a-z]/.test(password)) {
    $(this).addClass("border-danger");
    $(this)
      .next(".password-strength")
      .text("Password must contain at least one lowercase letter.")
      .addClass("text-danger");
    return;
  }

  // Check if the password contains at least one digit.
  if (!/[0-9]/.test(password)) {
    $(this).addClass("border-danger");
    $(this)
      .next(".password-strength")
      .text("Password must contain at least one digit.")
      .addClass("text-danger");
    return;
  }

  // Check if the password contains any spaces.
  if (/ /.test(password)) {
    $(this).addClass("border-danger");
    $(this)
      .next(".password-strength")
      .text("Password must not contain any spaces.")
      .addClass("text-danger");
    return;
  }

  // The password meets all the requirements.
  $(this).removeClass("border-danger");
  $(this)
    .next(".password-strength")
    .text("Password is strong.")
    .addClass("text-success")
    .removeClass("text-danger");

  $("#password2").keyup(function () {
    if ($("#password1").val() != $("#password2").val()) {
      $("#password2").addClass("border-danger");
      $("#password2")
        .next(".password-strength")
        .text("Password does not match")
        .addClass("text-danger");
      return;
    }
    $("#password2").removeClass("border-danger");
    $("#password2")
      .next(".password-strength")
      .text("")
      .removeClass("text-danger");
  });
});

$("#profile_page").ready(function () {
  $("#profile_details").load("/profile_details/");
});

$("#product").ready(function () {
  $("#product_table").load("/product_table/");
  $("#category_details").load("/category_details/");
  $("#product_form").load("/product_form/");
});

$("#order").ready(function () {
  $("#order_table").load("/order_table/");
});

$("#user").ready(function () {
  $("#user_table").load("/user_table/");
});

$("#customer").ready(function () {
  $("#customer_order_table").load("/customer_order_table/");
});

$("#customer_profile_page").ready(function () {
  $("#profile_details").load("/profile_details/");
});

// Retrieve the CSRF token value from the cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Check if the cookie name matches the CSRF token cookie name (default is 'csrftoken')
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function change_status_priv(event, id, action) {
  $.ajax({
    timeout: 5000,
    url: "/send_data/",
    data: { id: id, action: action, value: event.target.value },
    type: "post",

    beforeSend: function (xhr) {
      //add csrftoken to the request header
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    success: function (response) {
      toastr.success("Updated Succesfully!");
    },
    error: function (error) {
      toastr.error("Request Failed, Please try again.");
    },
  });
}

function get_data(data) {
  for (const key of Object.keys(data)) {
    if (key == "select_option") {
      for (const optionkey of Object.keys(data.select_option)) {
        $(`#${optionkey} option[value=${data.select_option[optionkey]}]`).attr(
          "selected",
          true
        );
      }
    }
    if (key == "image") {
      for (const imagekey of Object.keys(data.image)) {
        $("#" + imagekey).attr("src", data.image[imagekey]);
      }
    }
    if (key == "modal") {
      $("#" + data[key]).modal("show");
    }
    $("#" + key).val(data[key]);
  }
}
function preview_image(event) {
  var reader = new FileReader();
  reader.onload = function () {
    var img = event.target.previousElementSibling;
    event.target.nextElementSibling.nextElementSibling.innerHTML =
      event.target.value.split("\\").pop();
    img.src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
}

$("#delete_category").click(function (event) {
  let $btn = $(this);
  $.ajax({
    timeout: 5000,
    url: "/delete_category/",
    type: "post",
    data: { id: $("#edit_category_id").val() },
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    success: function (response) {
      $btn.html($btn.attr("data-name"));
      $btn.attr("disabled", false);
      if (response.message == "success") {
        toastr.success(response.info);
        if (response.modal) {
          setTimeout($("#" + response.modal).modal("hide"), 100);
        }
        if (response.pg) {
          response.pg.map((page) => {
            return $("#" + page).load("/" + page + "/");
          });
        } else {
          window.location = response.url_to;
        }
      } else {
        toastr.error(response.info);
      }
    },
    error: function (error) {
      $btn.html($btn.attr("data-name"));
      $btn.attr("disabled", false);
      toastr.error("Request failed, please try again");
    },
  });
});

$(".reg_login_form").submit(function (event) {
  event.preventDefault();
  let $form = $(this);
  let $url = $form.attr("action");
  let $btn = $form.find(".submit_btn");

  $.ajax({
    url: $url,
    timeout: 5000,
    type: "POST",
    data: new FormData(this),
    processData: false,
    contentType: false,
    beforeSend: function () {
      $btn.val("Processing...");
      $btn.attr("disabled", true);
    },
    success: function (response) {
      $btn.val($btn.attr("data-name"));
      $btn.attr("disabled", false);
      if (response.message == "success") {
        toastr.success(response.info);
        if (response.modal) {
          setTimeout($("#" + response.modal).modal("hide"), 100);
        }
        if (response.pg) {
          response.pg.map((page) => {
            return $("#" + page).load("/" + page + "/");
          });
        } else {
          window.location = response.url_to;
        }
      } else {
        toastr.error(response.info);
      }
    },
    error: function (error) {
      $btn.val($btn.attr("data-name"));
      $btn.attr("disabled", false);
      toastr.error("Request failed, please try again");
    },
  });
});

function customer_table_script() {
  //customer_table datatable
  $(document).ready(function () {
    $("#customer_table").DataTable({
      scrollY: 200,
      scrollX: true,
    });
  });

  //cancel and reorder button
  $(".cancel_reorder_btn").click(function () {
    let button = $(this);
    let id = button.attr("data-id");
    if (button.html() == "Cancel Order") {
      status = "Canceled";
      button_text = "Reorder";
      info = "Order Canceled!";
      button_action = button
        .html(button_text)
        .addClass("theme-bg")
        .removeClass("theme-bg2");
      status_action = button
        .parent(".actions")
        .siblings("td.status")
        .html(status)
        .addClass("text-danger")
        .removeClass("text-muted");
    } else {
      status = "Pending";
      button_text = "Cancel Order";
      info = "Order Restored";
      button_action = button
        .html(button_text)
        .addClass("theme-bg2")
        .removeClass("theme-bg");
      status_action = button
        .parent(".actions")
        .siblings("td.status")
        .html(status)
        .addClass("text-muted")
        .removeClass("text-danger");
    }
    $.ajax({
      url: "/change_order_status/",
      type: "post",
      data: { id: id, status: status },
      beforeSend: function (xhr, setting) {
        //to include the csrftoken in the request header
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function (response) {
        status_action;
        button_action;
        toastr.info(info);
      },
    });
  });
}
