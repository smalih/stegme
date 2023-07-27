$(function () {
  $('#toggleUserRegister').click(function (event) {
    toggleOrganiserDiv(event)
  })
})

$(function () {
  $('.close').click(function (event) {
    $(this).closest('div').remove()
  })
})

$(function toggleOrganiserDiv(event) {
  $('#organiserCodeDiv').toggleClass('hidden')
  if ($('#organiserCodeDiv').hasClass('hidden')) {
    $('#toggleUserButton').text('organiser')
  } else {
    $('#toggleUserButton').text('attendee')
  }
});

$('#register-event-form').on('submit', function(e) {
  e.preventDefault();
  $('#register-event-form').remove();
});

$(function redirectAddEvent() {
    $('#add-event-button').click(function(event) {
        location.href='/addevent';
    })
});

$(function () {
    $('.cancel-event-button').click(function(event) {
        $(this).disabled = true;
    });
})

$(function () {
    console.log($('.notification-form').length)
})