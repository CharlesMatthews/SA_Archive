//Start with first item (0)
let counter = 0;
// How many posts to load each time - In this case 10
const quantity = 10;

// When DOM loads, render posts.
document.addEventListener('DOMContentLoaded', load);

// If scrolled to bottom, load the next posts.
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

// If hide button is clicked, then "delete" the post.
document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'hide') {
        element.parentElement.style.animationPlayState = 'running';
        element.parentElement.addEventListener('animationend', () =>  {
            element.parentElement.remove();
        });
    }
});

// Load next set of posts.
function load() {
    // Set start and end post numbers, and update counter.
    const offset = counter;
    const end = offset + quantity - 1;
    counter = end + 1;
    console.log(offset)
    console.log(end)

    //Get the user's archive of tweets we are viewing from the URL.
    var Pagestring = window.location.pathname
    var token = document.getElementById("token").innerHTML
    var res = Pagestring.split("/");
    var urlr = '/api/' +res[2] +'/tweets?offset=' + offset +'&end='+end +'&token='+ token
    console.log(urlr)

    // Open a new request to get posts.
    const request = new XMLHttpRequest();
    request.open('GET', urlr);
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        data.forEach(add_post);
    };
    // Send request to url.
    request.send();
};

// Add a new post with given contents to DOM.
const post_template = Handlebars.compile(document.querySelector('#post').innerHTML);
function add_post(contents) {

    // Create new post.
    const post = post_template({'contents': contents});

    // Add post to DOM.
    document.querySelector('#posts').innerHTML += post;
};
