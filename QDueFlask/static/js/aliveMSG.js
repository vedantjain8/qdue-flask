$(document).ready(function() {
    $.ajax({
      url: '/QDueFlask/api/update_activity',
      type: 'POST',
      contentType: 'application/json',
      success: function(response) {
        console.log('Activity updated');
      },
      error: function(error) {
        console.log('Error updating activity');
      }
    });
  });

setInterval(sendActivity, 60000); // Send activity every minute
function sendActivity() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/QDueFlask/api/update_activity', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('Activity updated');
        } else {
            console.log('Error updating activity');
        }
    };
    xhr.send();
}
