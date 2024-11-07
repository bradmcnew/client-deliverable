// app.js
// Function to toggle the 'open' attribute based on window width
function toggleDetails() {
  const raceResults = document.getElementById("race-results");
  const rosterNav = document.getElementById("roster");
  if (window.innerWidth > 1000) {
    raceResults.setAttribute("open", "true");
    rosterNav.setAttribute("open", "true");
  } else {
    raceResults.removeAttribute("open");
    rosterNav.removeAttribute("open");
  }
}

// Function to update summary text based on details state
function updateSummaryText() {
  const raceResults = document.getElementById("race-results");
  const summary = raceResults.querySelector("summary");

  if (raceResults.hasAttribute("open")) {
    summary.textContent = "Click to collapse Race Results"; // When open
  } else {
    summary.textContent = "Click to expand Race Results"; // When closed
  }
}
// function to toggle the 'enlarged' class on the image
const image = document.getElementById("profileImage");

// Add an event listener for the click event
image.addEventListener("click", function () {
  // Toggle the 'enlarged' class on the image
  image.classList.toggle("enlarged");
});

// Run on page load and when the window is resized
window.addEventListener("load", () => {
  toggleDetails(); // Set initial state based on window width
  updateSummaryText(); // Update summary text based on details state
});

window.addEventListener("resize", () => {
  toggleDetails(); // Adjust details visibility on window resize
  updateSummaryText(); // Update summary text on resize
});

// Also, listen for when the details tag is toggled manually (if user clicks)
document
  .getElementById("race-results")
  .addEventListener("toggle", updateSummaryText);
