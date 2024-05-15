document.addEventListener("DOMContentLoaded", function() {
    var userLinks = document.querySelectorAll(".user-link");
    userLinks.forEach(function(link) {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            var commitsList = event.target.nextElementSibling;
            if (commitsList.style.display === "none") {
                commitsList.style.display = "block";
            } else {
                commitsList.style.display = "none";
            }
        });
    });
});