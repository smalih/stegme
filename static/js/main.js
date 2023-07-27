// $(function () {
//   $('#toggleUserRegister').click(function (event) {
//     toggleOrganiserDiv(event)
//   })
// })

$(function () {
  $('.close').click(function (event) {
    $(this).closest('div').remove()
  })
})

// $(function toggleOrganiserDiv(event) {
//   $('#organiserCodeDiv').toggleClass('hidden')
//   if ($('#organiserCodeDiv').hasClass('hidden')) {
//     $('#toggleUserButton').text('organiser')
//   } else {
//     $('#toggleUserButton').text('attendee')
//   }
// });

// $('#register-event-form').on('submit', function(e) {
//   e.preventDefault();
//   $('#register-event-form').remove();
// });

// $(function redirectAddEvent() {
//     $('#add-event-button').click(function(event) {
//         location.href='/addevent';
//     })
// });

// $(function () {
//     $('.cancel-event-button').click(function(event) {
//         $(this).disabled = true;
//     });
// })

// $(function () {
//     console.log($('.notification-form').length)
// })

$(document).ready(function(){
    var visible = false;
    var value = $("#one").text();


    $("#one").text('*'.repeat(value.length));

    $('#two').click(function() {
        if(visible){
            // value = $("#one").text();
            $("#one").text('*'.repeat(value.length));
            $("#two").text("Show")
        }else{
            $("#one").text(value);
            $("#two").text("Hide")
        }

        visible = !visible;
    });
});
