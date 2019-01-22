//document.addEventListener('DOMContentLoaded', loaddash);



//function getdata(url, id) {
//  var xhr = new XMLHttpRequest();

//  xhr.onreadystatechange = function() {
//    if (xhr.readyState === 4) {
//      console.log(xhr.response);
//      var value = xhr.response;
//      console.log(value);
//      add_post(id, xhr.response);
//      return value;
//    }
//  }

//  xhr.open('GET', url, true);
//  xhr.send('');



//}

//function loaddash() {
//  var token = document.getElementById("token").innerHTML///
//
//
//  var apitoptweets='/api/*/toptweet?end=3&token=' + token;
 //getdata(apitoptweets, "#toptweet");
  //console.log(x);
//
//
//  var apirecenttweets='/api/*/tweets?end=3&token=' + token;
//  add_post("#recent",getdata(apirecenttweets));
//
//  var apirandom='/api/*/tweets?end=1&random=true&token=' + token;
//  add_post("#random",getdata(apirandom));

//}




//function add_post(id, contents) {

//  var post_template = Handlebars.compile(document.querySelector(id).innerHTML);

//    // Create new post.
//    const post = post_template({'contents': contents});

//    // Add post to DOM.
//    document.querySelector(id).innerHTML += post;
//};
