document.addEventListener("DOMContentLoaded", function(event) { 
	var feedback_form = document.forms[1]
	var feedback_form_token = feedback_form.elements[1].value
	var csrfmiddlewaretoken = feedback_form.elements[0].value
	var found_useful_label = feedback_form.elements[3].label
	found_useful_label.style.display = 'none'
	document.querySelector('[name=found_useful]').click(function(el) {
	    var found_useful = document.querySelector(this).value;
	    fetch('/feedback/submit_initial/', {
		method: "POST",
		body: JSON.stringify(data),
		found_useful: found_useful,
		token: feedback_form_token,
		csrfmiddlewaretoken: csrfmiddlewaretoken,
		source_url: window.location.pathname
	    }).then(res => {
		console.log(body);
	    });
	});
});
    
var found_useful = feedback_form.elements[3].value
var comments = feedback_form.elements[8]

if (found_useful.value = undefined) {
	comments.style.display = 'none'
	found_useful.click(function() {
		comments.style.display = ''
	})
}



// TODO: this could be move to the design system in theory
function checkAndOpenDetails() {
  const hash = window.location.hash; // Get the current hash.
  if (hash) {
    const targetElement = document.querySelector(hash); // Find the element with the ID.
    if (targetElement) {
      // Check if the target is within a <details> element.
      const parentDetails = targetElement.closest('details');
      if (parentDetails) {
        parentDetails.open = true; // Open the <details> element.
      }
    }
  }
}
// Run the function on page load.
window.onload = checkAndOpenDetails;

// Optional: if you want to open the details when the hash changes without reloading the page.
window.onhashchange = checkAndOpenDetails;
