var random_messages = [
      "Amazing things come to those who wait",
      "You usually have to wait for that which is worth waiting for",
      "If you spend your whole life waiting for the storm, you'll never enjoy the sunshine",
      "Don't wait for the perfect moment. Take the moment and make it perfect",
      "Don't wait for opportunity. Create it.",
      "Glorious things are waiting for you. We're just getting them ready.",
      "Enjoy data responsibly... (Ish)",
      "Hello there friend 🙂",
      "function RandomisedMessage() {      var loading_message = random_messages[Math.floor(Math.random() * random_messages.length)];      return loading_message      //window.loading_screen.updateLoadingHtml(' "
                  ]


function RandomisedMessage() {
  //Picks a random message from the above array
      var loading_message = random_messages[Math.floor(Math.random() * random_messages.length)];
      return loading_message;
      //window.loading_screen.updateLoadingHtml('<p class="loading-message">' + loading_message + '</p> <div class="sk-spinner sk-spinner-rotating-plane"></div>');
    };


var random_images_array = ['SA.svg', 'SA1.svg', 'SA2.svg', 'SA3.svg'];

function getRandomImage(imgAr, path) {
  //Picks a random image from the above array
    path = '/static/images/'; // Path to folder of images
    var num = Math.floor( Math.random() * imgAr.length ); // Picks a random number within the array's length
    var img = imgAr[ num ]; //Sets the image variable to the item within the list picked out
    var imgStr = path + img; //Sets imgStr to the filepath
    document.getElementById("brand").src=imgStr;  //Writes to the HTML document the new file path -> retrieved by browser
    document.close();
}


function PWWindowInitialLoad(){
  var message = RandomisedMessage() //Gets a randomised message and stores to variable
  window.loading_screen = window.pleaseWait({
            logo: "/static/images/SA2.svg",
            backgroundColor: '#cc0841',
            loadingHtml: '<p class="loading-message">'+message+'</p> <div class="sk-spinner sk-spinner-rotating-plane"></div>'
          });
        };


function PWWindowHandler(){
  PWWindowInitialLoad()
  getRandomImage(random_images_array, '/images/')
  var elements = document.getElementsByClassName('btn btn-outline-light');
  window.onload = function() {
    //When loaded
    setTimeout(window.loading_screen.finish(), 10);
    //Close the loading screen
    console.log("Don’t worry so much about money. Worry about if people start deciding to kill reporters. That's a quote. For the reason why, you can say I want reporters to know I make more money than them, especially Matt Pearce.")
  };
}



function setCaretPosition(ctrl, pos) {
  // Modern browsers
  if (ctrl.setSelectionRange) {
    ctrl.focus();
    ctrl.setSelectionRange(pos, pos);

  // IE8 and below
  } else if (ctrl.createTextRange) {
    var range = ctrl.createTextRange();
    range.collapse(true);
    range.moveEnd('character', pos);
    range.moveStart('character', pos);
    range.select();
  }
}

function openSearch() {
    document.getElementById("myOverlay").style.display = "block";
    var input = document.getElementById('search');
    setCaretPosition(input, input.value.length);
}

function closeSearch() {
    document.getElementById("myOverlay").style.display = "none";
}


//            loadingHtml: '<p class="loading-message"> You usually have to wait for that which is worth waiting for </p> <div class="sk-spinner sk-spinner-rotating-plane"></div>'

//updateLoadingHtml('<p>Please login in order to proceed</p> <form action="http://' + window.location.hostname  +'/login" method="post"> <div class="form-group"> <input class="form-control" name="Email" placeholder="Email"> </div><div class="form-group"><input class="form-control" input type="password" name="Password" placeholder="Password"></div><div class="form-group"><button class="btn btn-primary">Login!</button></div></form>');
//
//var elements = document.getElementsByClassName('btn btn-outline-light');
//if (elements[0].innerHTML = "Login!"){
//  window.loading_screen.updateLoadingHtml('<p>Please login in order to proceed</p>' +
//  '<form action="http://' + window.location.hostname  +'/login" method="post">'+
//      '<div class="form-group">' +
//          '<input class="form-control" name="Email" placeholder="Email">' +
//      '</div>' +
//      '<div class="form-group">' +
//          '<input class="form-control" input type="password" name="Password" placeholder="Password">' +
//      '</div>' +
//      '<div class="form-group">' +
//          '<button class="btn btn-primary">Login!</button>' +
//      '</div>' +
//  '</form>');
//} else {
//  var interval = setInterval(RandomisedMessage, 150);
//}

//updateLoadingHtml('<p>Please login in order to proceed</p>' +
//'<form action="http://' + window.location.hostname  +'/login" method="post">'+
//    '<div class="form-group">' +
//        '<input class="form-control" name="Email" placeholder="Email">' +
//    '</div>' +
//    '<div class="form-group">' +
//        '<input class="form-control" input type="password" name="Password" placeholder="Password">' +
//    '</div>' +
//    '<div class="form-group">' +
//        '<button class="btn btn-primary">Login!</button>' +
//    '</div>' +
//'</form>');
//};
//      break;
//    default:
//
//  }
//  if
//  window.loading_screen.finish();
//};
